from flask import jsonify, request
from flask_restful import Resource
from app.models import Users, DietData
from app.schemas.user import UserSchema, DietDataSchema

user_schema = UserSchema(many=True)
diet_data_schema = DietDataSchema(many=True)


class AllUsersWithDietData(Resource):
    def get(self):
        # Fetch all users
        users = Users.query.all()
        users_data = user_schema.dump(users)

        # Fetch all diet data
        diet_data = DietData.query.all()
        diet_data_records = diet_data_schema.dump(diet_data)

        # Organize data per user
        user_diet_mapping = {}
        for user in users_data:
            user_id = user["id"]
            user_diet_mapping[user_id] = {
                "user_info": user,
                "diet_data": [],
            }

        for diet in diet_data_records:
            user_id = diet["user_id"]
            if user_id in user_diet_mapping:
                user_diet_mapping[user_id]["diet_data"].append(diet)

        # Convert mapping to list
        final_output = list(user_diet_mapping.values())

        return jsonify(final_output)


class UserDietByID(Resource):
    def get(self, user_id):
        """Returns a specific user's diet data based on user ID in the path."""
        # Fetch diet data for the specified user
        user_diets = DietData.query.filter_by(user_id=user_id).all()
        
        if not user_diets:
            return {"message": "No diet records found for this user"}, 404

        return {"diet_data": diet_data_schema.dump(user_diets)}, 200


class UserDietByQuery(Resource):
    def get(self):
        """Returns a specific user's diet data based on user ID passed as a query parameter."""
        user_id = request.args.get("user_id")

        if not user_id:
            return {"message": "User ID is required as a query parameter"}, 400
        
        # Fetch diet data for the specified user
        user_diets = DietData.query.filter_by(user_id=user_id).all()
        
        if not user_diets:
            return {"message": "No diet records found for this user"}, 404

        return {"diet_data": diet_data_schema.dump(user_diets)}, 200
