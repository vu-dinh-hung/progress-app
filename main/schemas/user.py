"""Module for marshmallow schemas for user"""
from marshmallow import Schema, fields, validate, ValidationError
from marshmallow.decorators import post_load
from main.schemas.base import BaseSchema
from main.utils.password import hash_password


def validate_password(password):
    """Validate a password"""
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters")
    if " " in password:
        raise ValidationError("Password must not contain whitespace")


class UserSchema(BaseSchema):
    """Schema for validating user response data"""

    username = fields.String(dump_only=True)
    name = fields.String()
    password = fields.String(load_only=True, validate=[validate_password])

    @post_load
    def make_password_hash(
        self, data, **kwargs
    ):  # pylint: disable=no-self-use,unused-argument
        """Replace password with password_hash on deserialization"""
        if data.get("password"):
            data["password_hash"] = hash_password(data["password"])
            data.pop("password", None)
        return data


class PostUserSchema(UserSchema):
    """Schema for validating user POST request data"""

    min_username, max_username = 4, 30

    username = fields.String(
        required=True,
        load_only=True,
        validate=[
            validate.Length(
                min=min_username,
                max=max_username,
                error=f"Username must be between {min_username} and {max_username} characters",
            )
        ],
        error_messages={"required": "Username required"},
    )
    password = fields.String(
        required=True,
        load_only=True,
        validate=[validate_password],
        error_messages={"required": "Password required"},
    )


class PutUserSchema(UserSchema):
    """Schema for validating user PUT request data"""


class LoginSchema(Schema):
    """Schema for validating login request data"""

    username = fields.String(
        required=True, load_only=True, error_messages={"required": "Username required"}
    )
    password = fields.String(
        required=True, load_only=True, error_messages={"required": "Password required"}
    )


user_schema = UserSchema()
login_schema = LoginSchema()
post_user_schema = PostUserSchema()
put_user_schema = PutUserSchema()
