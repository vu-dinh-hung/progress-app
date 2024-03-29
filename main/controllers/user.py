"""Module for user_router blueprint"""
# pylint: disable=unused-argument
from flask import Blueprint
from flask_jwt_extended import create_access_token
from main.models.user import User
from main.engines.user import update_user, create_user, get_user_by_username
from main.schemas.user import (
    user_schema,
    post_user_schema,
    put_user_schema,
    login_schema,
)
from main.utils.decorators import load_data, verify_user
from main.utils.password import check_password
from main.exceptions import UnauthorizedError

user_router = Blueprint("user_router", __name__)


@user_router.route("/login", methods=["POST"])
@load_data(login_schema)
def login(data: dict):
    """POST login"""
    user = get_user_by_username(data["username"])
    if not user or not check_password(data["password"], user.password_hash):
        raise UnauthorizedError("Wrong username or password")

    access_token = create_access_token(identity=user.id, fresh=True)

    return {"access_token": access_token, "user": user_schema.dump(user)}, 200


@user_router.route("/users", methods=["POST"])
@load_data(post_user_schema)
def post(data: dict):
    """POST user"""
    user = create_user(**data)

    return user_schema.dump(user), 201


@user_router.route("/users/<int:user_id>", methods=["GET"])
@verify_user
def get(user_id: int, user: User):
    """GET user"""
    return user_schema.dump(user), 200


@user_router.route("/users/<int:user_id>", methods=["PUT"])
@load_data(put_user_schema)
@verify_user
def put(user_id: int, user: User, data: dict):
    """PUT user"""
    updated_user = update_user(user, data)

    return user_schema.dump(updated_user), 200
