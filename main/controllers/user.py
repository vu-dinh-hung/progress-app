"""Module for user_router blueprint"""
from flask import Blueprint
from flask_jwt_extended import create_access_token
from main.engines.user import UserEngine
from main.schemas.user import user_schema, new_user_schema, login_schema
from main.utils.decorators import load_data, verify_user
from main.utils.password import check_password
from main.exceptions import UnauthorizedError, NotFoundError

user_router = Blueprint("user_router", __name__)


@user_router.route("/login", methods=["POST"])
@load_data(login_schema)
def login(data):
    """POST login"""
    user = UserEngine.find_by_username(data["username"])
    if not user or not check_password(data["password"], user.password_hash):
        raise UnauthorizedError("Wrong username or password")

    access_token = create_access_token(identity=user.id, fresh=True)

    return {"access_token": access_token, "user": user_schema.dump(user)}, 200


@user_router.route("/users", methods=["POST"])
@load_data(new_user_schema)
def post_user(data):
    """POST user"""
    user = UserEngine.create_user(**data)

    return user_schema.dump(user), 201


@user_router.route("/users/<int:user_id>", methods=["GET"])
@verify_user
def get_user(user_id):
    """GET user"""
    user = UserEngine.find_by_id(user_id)
    if not user:
        raise NotFoundError("User not found")

    return user_schema.dump(user), 200


@user_router.route("/users/<int:user_id>", methods=["PUT"])
@load_data(user_schema)
@verify_user
def put_user(data, user_id):
    """PUT user"""
    UserEngine.update_by_id(user_id, data)
    user = UserEngine.find_by_id(user_id)

    return user_schema.dump(user), 200
