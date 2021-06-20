"""Module for user_router blueprint"""
# pylint: disable=unused-argument
from flask import Blueprint
from flask_jwt_extended import create_access_token
from main.engines.user import get_user, update_user, create_user, get_user_by_username
from main.schemas.user import user_schema, new_user_schema, login_schema
from main.utils.decorators import load_data, verify_user
from main.utils.password import check_password
from main.exceptions import UnauthorizedError

user_router = Blueprint("user_router", __name__)


@user_router.route("/login", methods=["POST"])
@load_data(login_schema)
def login(data):
    """POST login"""
    user = get_user_by_username(data["username"])
    if not user or not check_password(data["password"], user.password_hash):
        raise UnauthorizedError("Wrong username or password")

    access_token = create_access_token(identity=user.id, fresh=True)

    return {"access_token": access_token, "user": user_schema.dump(user)}, 200


@user_router.route("/users", methods=["POST"])
@load_data(new_user_schema)
def post(data):
    """POST user"""
    user = create_user(**data)

    return user_schema.dump(user), 201


@user_router.route("/users/<int:user_id>", methods=["GET"])
@verify_user
def get(user_id, user):
    """GET user"""
    return user_schema.dump(user), 200


@user_router.route("/users/<int:user_id>", methods=["PUT"])
@load_data(user_schema)
@verify_user
def put(user_id, user, data):
    """PUT user"""
    update_user(user.id, data)
    user = get_user(user.id)

    return user_schema.dump(user), 200
