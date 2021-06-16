from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from main.models.habit import Habit

def jwt_required_verify_user():
    def wrapper(fn):
        @wraps(fn)
        def decorator(user_id, *args, **kwargs):
            verify_jwt_in_request()
            jwt_id = get_jwt_identity()
            if user_id == str(jwt_id):
                return fn(user_id, *args, **kwargs)
            else:
                return {'message': 'User not found'}, 404

        return decorator

    return wrapper

def jwt_required_verify_user_and_habit():
    def wrapper(fn):
        @wraps(fn)
        def decorator(user_id, habit_id, *args, **kwargs):
            verify_jwt_in_request()
            jwt_id = get_jwt_identity()

            if user_id != str(jwt_id):
                return {'message': 'User not found'}, 404

            habit = Habit.find_by_id(habit_id)
            if not habit or user_id != str(habit.user_id):
                return {'message': 'Habit not found'}, 404

            return fn(user_id, habit_id, *args, **kwargs)

        return decorator

    return wrapper
