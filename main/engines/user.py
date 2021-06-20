"""Module for user-related operations"""
from typing import Optional
from main.exceptions import BadRequestError
from main.models.user import User


def get_user(user_id: int) -> Optional[User]:
    """Return an user by id or None if user not found"""
    return User.find_by_id(user_id)


def update_user(user: User, data: dict) -> User:
    """Update an user by id"""
    User.update_by_id(user.id, data)
    return User.find_by_id(user.id)


def create_user(
    *, username: str, password_hash: str, name: Optional[str] = None
) -> User:
    """Create and save an user into database, then return the user"""
    user = get_user_by_username(username)
    if user:
        raise BadRequestError("Username already exists")

    user = User(username=username, password_hash=password_hash, name=name)
    user.save()
    return user


def get_user_by_username(username: str) -> Optional[User]:
    """Return the user with the given username or None if the username does not exist"""
    return User.query.filter_by(username=username).first()
