"""Module for helper decorators"""
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from main.models.habit import Habit


def jwt_required_verify_user():
    """Check whether jwt contains id that matches user_id in url"""

    def wrapper(func):
        @wraps(func)
        def decorator(user_id, *args, **kwargs):
            verify_jwt_in_request()
            jwt_id = get_jwt_identity()

            if user_id == jwt_id:
                return func(user_id, *args, **kwargs)

            return {"message": "User not found"}, 404

        return decorator

    return wrapper


def jwt_required_verify_user_and_habit():
    """Check that jwt id matches user_id, and check that user owns given habit_id"""

    def wrapper(func):
        @wraps(func)
        def decorator(user_id, habit_id, *args, **kwargs):
            verify_jwt_in_request()
            jwt_id = get_jwt_identity()

            if user_id != jwt_id:
                return {"message": "User not found"}, 404

            habit = Habit.find_by_id(habit_id)
            if not habit or user_id != habit.user_id:
                return {"message": "Habit not found"}, 404

            return func(user_id, habit_id, *args, **kwargs)

        return decorator

    return wrapper
