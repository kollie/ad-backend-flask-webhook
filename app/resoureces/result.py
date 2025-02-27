from flask import jsonify
from flask_restful import Resource
from app.models import Users, DietData
from app.schemas import UserSchema, DietDataSchema

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
