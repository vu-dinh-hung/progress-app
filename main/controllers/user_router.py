"""Module for user_router blueprint"""
from flask import Blueprint, request, jsonify
import bcrypt
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token
)
from main.models.user import User, user_schema, login_schema, new_user_schema

user_router = Blueprint('user_router', __name__)


@user_router.route('/login', methods=['POST'])
def login():
    body = request.get_json(force=True)
    errors = login_schema.validate(body)
    if errors:
        return {
            'message': 'Invalid credentials',
            'data': errors
        }, 401

    credentials = login_schema.load(body)
    user = User.find_by_username(credentials['username'])
    access_token = create_access_token(identity=user.id, fresh=True)

    return {
        'access_token': access_token,
        'user': user_schema.dump(user)
    }


@user_router.route('/users', methods=['POST'])
def post_user():
    body = request.get_json(force=True)
    errors = new_user_schema.validate(body)
    if errors:
        return {
            'message': 'Invalid field(s)',
            'data': errors
        }, 400

    user_data = new_user_schema.load(body)
    password_hash = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt(14))
    user = User(**user_data, password_hash=password_hash)
    user.save()

    return user_schema.dump(user), 201


@user_router.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    jwt_id = get_jwt_identity()
    if user_id != str(jwt_id):
        return {'message': 'User not found'}, 404

    user = User.find_by_id(user_id)
    if user:
        return user.to_dict()
    else:
        return {'message': 'User not found'}, 404


@user_router.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def put_user(user_id):
    jwt_id = get_jwt_identity()
    if user_id != str(jwt_id):
        return {'message': 'User not found'}, 404

    body = request.get_json(force=True)
    errors = user_schema.validate(body)
    if errors:
        return {
            'data': errors
        }, 400

    User.update(user_id, user_schema.load(body))
    user = User.find_by_id(user_id)
    return user_schema.dump(user), 200
