"""Module for user_router blueprint"""
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from main.models.user import User
from main.schemas.user_schema import user_schema, new_user_schema, login_schema
from main.utils.decorators import jwt_required_verify_user

user_router = Blueprint("user_router", __name__)


@user_router.route("/login", methods=["POST"])
def login():
    """POST login"""
    body = request.get_json(force=True)
    errors = login_schema.validate(body)
    if errors:
        return {"message": "Missing field(s)", "data": errors}, 401

    credentials = login_schema.load(body)
    user = User.find_by_username(credentials["username"])
    if not user or not user.check_password(credentials["password"]):
        return {"message": "Wrong username or password"}, 401

    access_token = create_access_token(identity=user.id, fresh=True)

    return {"access_token": access_token, "user": user_schema.dump(user)}, 200


@user_router.route("/users", methods=["POST"])
def post_user():
    """POST user"""
    body = request.get_json(force=True)
    errors = new_user_schema.validate(body)
    if errors:
        return {"message": "Invalid field(s)", "data": errors}, 400

    user_data = new_user_schema.load(body)
    user = User(**user_data)
    user.save()

    return user_schema.dump(user), 201


@user_router.route("/users/<user_id>", methods=["GET"])
@jwt_required_verify_user()
def get_user(user_id):
    """GET user"""
    user = User.find_by_id(user_id)
    if not user:
        return {"message": "User not found"}, 404

    return user_schema.dump(user), 200


@user_router.route("/users/<user_id>", methods=["PUT"])
@jwt_required_verify_user()
def put_user(user_id):
    """PUT user"""
    body = request.get_json(force=True)
    errors = user_schema.validate(body)
    if errors:
        return {"data": errors}, 400

    update_data = user_schema.load(body)
    User.update_by_id(user_id, update_data)
    user = User.find_by_id(user_id)

    return user_schema.dump(user), 200
