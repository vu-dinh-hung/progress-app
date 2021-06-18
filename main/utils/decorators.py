"""Module for helper decorators"""
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from main.engines.user import UserEngine
from main.engines.habit import HabitEngine
from main.exceptions import NotFoundError


def verify_user(func):
    """Check whether jwt contains id that matches user_id in url"""

    @wraps(func)
    def modified_func(user_id, *args, **kwargs):
        verify_jwt_in_request()
        jwt_id = get_jwt_identity()
        if user_id != jwt_id or not UserEngine.find_by_id(user_id):
            raise NotFoundError("User not found")

        return func(user_id, *args, **kwargs)

    return modified_func


def verify_habit(func):
    """Check that user owns given habit_id. Should be used after @verify_user"""

    @wraps(func)
    def modified_func(user_id, habit_id, *args, **kwargs):
        habit = HabitEngine.find_by_id(habit_id)
        if not habit or user_id != habit.user_id:
            raise NotFoundError("Habit not found")

        return func(user_id, habit_id, *args, **kwargs)

    return modified_func
