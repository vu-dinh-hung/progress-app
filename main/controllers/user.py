"""Module for user_router blueprint"""
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from main.engines.user import UserEngine
from main.schemas.user import user_schema, new_user_schema, login_schema
from main.utils.decorators import jwt_required_verify_user
from main.utils.password import check_password
from main.exceptions import BadRequestError, UnauthorizedError, NotFoundError

user_router = Blueprint("user_router", __name__)


@user_router.route("/login", methods=["POST"])
def login():
    """POST login"""
    body = request.get_json(force=True)
    errors = login_schema.validate(body)
    if errors:
        raise BadRequestError("Missing field(s)", errors)

    credentials = login_schema.load(body)
    user = UserEngine.find_by_username(credentials["username"])
    if not user or not check_password(credentials["password"], user.password_hash):
        raise UnauthorizedError("Wrong username or password")

    access_token = create_access_token(identity=user.id, fresh=True)

    return {"access_token": access_token, "user": user_schema.dump(user)}, 200


@user_router.route("/users", methods=["POST"])
def post_user():
    """POST user"""
    body = request.get_json(force=True)
    errors = new_user_schema.validate(body)
    if errors:
        raise BadRequestError("Invalid field(s)", errors)

    user_data = new_user_schema.load(body)
    user = UserEngine.create_user(**user_data)

    return user_schema.dump(user), 201


@user_router.route("/users/<int:user_id>", methods=["GET"])
@jwt_required_verify_user()
def get_user(user_id):
    """GET user"""
    user = UserEngine.find_by_id(user_id)
    if not user:
        raise NotFoundError("User not found")

    return user_schema.dump(user), 200


@user_router.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required_verify_user()
def put_user(user_id):
    """PUT user"""
    body = request.get_json(force=True)
    errors = user_schema.validate(body)
    if errors:
        raise BadRequestError("Invalid field(s)", errors)

    update_data = user_schema.load(body)
    UserEngine.update_by_id(user_id, update_data)
    user = UserEngine.find_by_id(user_id)

    return user_schema.dump(user), 200
