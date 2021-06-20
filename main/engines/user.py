"""Module for user-related operations"""
from main.models.user import User


def get_user(user_id):
    """Return an user by id or None if user not found"""
    return User.find_by_id(user_id)


def update_user(user_id, data):
    """Update an user by id"""
    User.update_by_id(user_id, data)


def create_user(*args, **kwargs):
    """Create and save an user into database, then return the user"""
    user = User(*args, **kwargs)
    user.save()
    return user


def get_user_by_username(username):
    """Return the user with the given username or None if the username does not exist"""
    return User.query.filter_by(username=username).first()
