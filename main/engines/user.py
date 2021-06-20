"""Module for user-related operations"""
from main.exceptions import BadRequestError
from main.models.user import User


def get_user(user_id):
    """Return an user by id or None if user not found"""
    return User.find_by_id(user_id)


def update_user(user_id, data):
    """Update an user by id"""
    User.update_by_id(user_id, data)


def create_user(*, username, password_hash, name=None):
    """Create and save an user into database, then return the user"""
    user = get_user_by_username(username)
    if user:
        raise BadRequestError("Username already exists")

    user = User(username=username, password_hash=password_hash, name=name)
    user.save()
    return user


def get_user_by_username(username):
    """Return the user with the given username or None if the username does not exist"""
    return User.query.filter_by(username=username).first()
