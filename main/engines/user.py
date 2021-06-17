"""Module for UserEngine"""
from main.models.user import User


class UserEngine:
    """Engine class for providing user-related operations"""

    @staticmethod
    def find_by_id(*args, **kwargs):
        """Return an user by id or None if user not found"""
        return User.find_by_id(*args, **kwargs)

    @staticmethod
    def update_by_id(*args, **kwargs):
        """Update an user by id"""
        User.update_by_id(*args, **kwargs)

    @staticmethod
    def create_user(*args, **kwargs):
        """Create and save an user into database, then return the user"""
        user = User(*args, **kwargs)
        user.save()
        return user

    @staticmethod
    def find_by_username(username):
        """Return the user with the given username or None if the username does not exist"""
        return User.query.filter_by(username=username).first()
