from app import ma
from app.models import Users, DietData

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_only = ("password",)  # Exclude password when serializing
        dump_only = ("id",)  # Do not allow changing ID
        include_fk = True  # Include foreign keys
        load_instance = True  # Deserialize to model instance

class DietDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DietData
        dump_only = ("id", "created_at", "updated_at")  # Read-only fields
        include_fk = True  # Include foreign keys
        load_instance = True  # Deserialize to model instance
