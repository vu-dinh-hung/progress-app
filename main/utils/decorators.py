"""Module for helper decorators"""
from functools import wraps
from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from main.engines.user import UserEngine
from main.engines.habit import HabitEngine
from main.exceptions import BadRequestError, NotFoundError


def load_body(schema):
    """Validate and load request body"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.method == "GET":
                req_data = request.args
                error_message = "Invalid query parameter(s)"
            elif request.method == "PUT" or request.method == "POST":
                req_data = request.get_json(force=True)
                error_message = "Invalid field(s)"
            else:
                return func(*args, **kwargs)

            errors = schema.validate(req_data)
            if errors:
                raise BadRequestError(error_message, errors)

            data = schema.load(req_data)
            return func(*args, **kwargs, data=data)

        return wrapper

    return decorator


def verify_user(func):
    """Check whether jwt contains id that matches user_id in url"""

    @wraps(func)
    def wrapper(user_id, *args, **kwargs):
        verify_jwt_in_request()
        jwt_id = get_jwt_identity()
        if user_id != jwt_id or not UserEngine.find_by_id(user_id):
            raise NotFoundError("User not found")

        return func(*args, **kwargs, user_id=user_id)

    return wrapper


def verify_habit(func):
    """Check that user with user_id owns habit_id"""

    @wraps(func)
    def wrapper(user_id, habit_id, *args, **kwargs):
        habit = HabitEngine.find_by_id(habit_id)
        if not habit or user_id != habit.user_id:
            raise NotFoundError("Habit not found")

        return func(*args, **kwargs, user_id=user_id, habit_id=habit_id)

    return wrapper
