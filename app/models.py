from typing import List
from datetime import datetime, date, timedelta
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash


from app import app, db


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    username = db.Column(db.String(30))
    password = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

      # hash user password input
    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    # verify user password input hash with existing password hash
    def check_password(self, password: str):
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_username(cls, username: str) -> "Users":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "Users":
        return cls.query.filter_by(id=_id).first()
    
class DietData(db.Model):
    __tablename__ = 'diet_data'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key linking to Users table
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    activity_level = db.Column(db.String(20), nullable=False)
    goal = db.Column(db.String(20), nullable=False)
    dietary_preference = db.Column(db.String(20), nullable=False)
    predicted_diet = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())

    # Define relationship with Users table
    user = db.relationship('Users', backref=db.backref('diet_data', lazy=True))


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()



