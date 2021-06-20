"""Module for helper decorators"""
from functools import wraps
from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from main.engines.user import get_user
from main.engines.habit import get_habit
from main.engines.log import get_log
from main.exceptions import BadRequestError, NotFoundError


def load_data(schema):
    """Validate and load request body/query params

    View function should include a 'data' parameter.
    Argument:
    schema -- a schema to validate and load request data
    """

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
    """Check whether jwt contains id that matches user_id in url, and loads the user if successful

    View function should include a 'user' parameter.
    """

    @wraps(func)
    def wrapper(user_id, *args, **kwargs):
        verify_jwt_in_request()
        jwt_id = get_jwt_identity()
        error_message = "User not found"
        if user_id != jwt_id:
            raise NotFoundError(error_message)

        user = get_user(user_id)
        if not user:
            raise NotFoundError(error_message)

        return func(user_id, *args, **kwargs, user=user)

    return wrapper


def verify_habit(func):
    """Check that user with user_id owns habit_id, and loads the habit if successful

    View function should include a 'habit' parameter.
    """

    @wraps(func)
    def wrapper(user_id, habit_id, *args, **kwargs):
        habit = get_habit(habit_id)
        if not habit or user_id != habit.user_id:
            raise NotFoundError("Habit not found")

        return func(user_id, habit_id, *args, **kwargs, habit=habit)

    return wrapper


def verify_log(func):
    """Check that habit with habit_id owns log_id, and loads the log if successful

    View function should include a 'log' parameter.
    """

    @wraps(func)
    def wrapper(user_id, habit_id, log_id, *args, **kwargs):
        log = get_log(log_id)
        if not log or habit_id != log.habit_id:
            raise NotFoundError("Log not found")

        return func(user_id, habit_id, log_id, *args, **kwargs, log=log)

    return wrapper
