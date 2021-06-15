"""Module for User model"""
import bcrypt
from marshmallow import Schema, fields, validate, validates, ValidationError
from marshmallow.decorators import post_load
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

    @classmethod
    def find_by_username(cls, username):
        """Return the user with the given username
        or None if the username does not exist
        """
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def hash_password(password):
        """Return a secure hash for the given password"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))

    def check_password(self, password):
        """Compare the given password with the user's password_hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)


def validate_password(password):
    """Validate a password"""
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters')
    if ' ' in password:
        raise ValidationError('Password must not contain whitespace')


class UserSchema(BaseSchema):
    username = fields.String(dump_only=True)
    name = fields.String()
    password = fields.String(load_only=True, validate=[validate_password])

    @post_load
    def make_password_hash(self, data, **kwargs):
        if data.get('password'):
            data['password_hash'] = User.hash_password(data['password'])
            data.pop('password', None)
        return data


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
        error_messages={'required': 'Username required'}
    )
    password = fields.String(
        required=True,
        load_only=True,
        validate=[validate_password],
        error_messages={'required': 'Password required'}
    )
    name = fields.String()

    @validates('username')
    def check_duplicate_username(self, username, **kwargs):
        user = User.find_by_username(username)
        if user:
            raise ValidationError('Username already exist')

    @post_load
    def make_password_hash(self, data, **kwargs):
        data['password_hash'] = User.hash_password(data['password'])
        data.pop('password')
        return data


class LoginSchema(Schema):
    username = fields.String(
        required=True, load_only=True, error_messages={'required': 'Username required'}
    )
    password = fields.String(
        required=True, load_only=True, error_messages={'required': 'Password required'}
    )


user_schema = UserSchema()
login_schema = LoginSchema()
new_user_schema = NewUserSchema()
