"""Module for User model"""
import bcrypt
from marshmallow import Schema, fields, validate, validates_schema
from marshmallow.exceptions import ValidationError
from main.db import db, BaseSchema


class User(db.Model):
    """User Model for 'users' table"""
    __tablename__ = 'users'

    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(50), nullable=True)

    def __repr__(self) -> str:
        return f'<User(id={self.id}, username={self.username}, name={self.name}, ' +\
            f'status={self.status}, created_at={self.created_at}, updated_at={self.updated_at})>'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, User): return False
        if self.id != o.id: return False
        if self.username != o.username: return False
        if self.name != o.name: return False
        if self.password_hash != o.password_hash: return False
        return True

    @classmethod
    def find_by_username(cls, username):
        """Return the user with the given username
        or None if the username does not exist
        """
        return cls.query.filter_by(username=username).first()


class UserSchema(BaseSchema):
    username = fields.String(dump_only=True)
    name = fields.String()


class NewUserSchema(Schema):
    min_username, max_username = 4, 30
    username = fields.String(
        required=True,
        load_only=True,
        validate=[
            validate.Length(
                min=min_username, max=max_username,
                error=f'Username must be between {min_username} and {max_username} characters'
            )
        ],
        error_messages={'required': {'message': 'Username required'}}
    )
    password = fields.String(
        required=True,
        load_only=True,
        validate=[validate.Length(min=8, error='Password must be at least 8 characters')],
        error_messages={'required': {'message': 'Username required'}}
    )
    name = fields.String()


class LoginSchema(Schema):
    username = fields.String(required=True, load_only=True)
    password = fields.String(required=True, load_only=True)

    @validates_schema
    def check_credentials(self, data, **kwargs):
        errors = {}

        user = User.find_by_username(data['username'])
        if not user:
            errors['username'] = ['Wrong username']
        if user and not bcrypt.checkpw(data['password'].encode('utf-8'), user.password_hash):
            errors['password'] = ['Wrong password']

        if errors:
            raise ValidationError(errors)


user_schema = UserSchema()
login_schema = LoginSchema()
new_user_schema = NewUserSchema()
