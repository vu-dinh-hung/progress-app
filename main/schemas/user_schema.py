from marshmallow import Schema, fields, validate, validates, ValidationError
from marshmallow.decorators import post_load
from main.schemas.base_schema import BaseSchema
from main.models.user import User


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
