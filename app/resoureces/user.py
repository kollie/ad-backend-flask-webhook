from flask_restful import Resource
from flask import request
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from app.models.user import Users, DietData
from app.schemas.user import UserSchema, DietDataSchema

user_schema = UserSchema()
diet_data_schema = DietDataSchema()
diet_data_list_schema = DietDataSchema(many=True)

class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_data = request.get_json()

        # Validate and deserialize input
        user = user_schema.load(user_data)

        if Users.find_by_username(user.username):
            return {"message": "A user with that username already exists"}, 400

        # Set password hash
        user.set_password(user.password)

        # Save user to database
        user.save_to_db()

        return {"message": "User created successfully."}, 201
    
class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_data = request.get_json()
        
        # Deserialize input
        user = Users.find_by_username(user_data.get("username"))

        if not user or not user.check_password(user_data.get("password")):
            return {"message": "Invalid credentials"}, 401

        # Set token expiration time
        expires = datetime.now() + timedelta(hours=24)

        # Generate JWT tokens
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "user_id": user.id,
            "token_expires": expires.strftime("%Y-%m-%d %H:%M:%S.%f")
        }, 200
    


class DietDataResource(Resource):
    @jwt_required()  # Protect the route
    def post(self):
        user_id = get_jwt_identity()  # Get logged-in user ID from JWT

        # Deserialize request data
        diet_data = diet_data_schema.load(request.get_json())
        diet_data.user_id = user_id  # Assign user ID

        # Save to database
        diet_data.save_to_db()

        return {"message": "Diet data saved successfully", "diet_id": diet_data.id}, 201

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()  # Get logged-in user ID

        # Retrieve user's diet data
        user_diets = DietData.query.filter_by(user_id=user_id).all()

        if not user_diets:
            return {"message": "No diet records found for this user"}, 404

        return {"diet_data": diet_data_list_schema.dump(user_diets)}, 200

