"""Module for log_router blueprint"""
from flask import Blueprint, request
from main.models.habit import Habit
from main.models.log import Log
from main.schemas.log_schema import (
    log_schema, new_log_schema, new_log_with_count_schema
)
from main.utils.decorators import jwt_required_verify_user_and_habit

log_router = Blueprint('log_router', __name__)
base_url = '/users/<user_id>/habits/<habit_id>'


@log_router.route(f'{base_url}/logs', methods=['POST'])
@jwt_required_verify_user_and_habit()
def post_log(user_id, habit_id):
    habit = Habit.find_by_id(habit_id)
    if not habit or user_id != str(habit.user_id):
        return {'message': 'Habit not found'}, 404

    # load log schema according to countability of habit
    schema = new_log_with_count_schema if habit.countable else new_log_schema

    body = request.get_json(force=True)
    errors = schema.validate(body)
    if errors:
        return {
            "message": "Invalid field(s)",
            "data": errors
        }, 400

    log_data = schema.load(body)

    # if log for given date and habit already exist, set status of that log to 'active'
    log_in_db = Log.get_one(habit_id=habit_id, date=log_data['date'])
    log = None
    if log_in_db:
        print('found matching log')
        log_in_db.status = 'active'
        log_in_db.save()
        log = log_in_db
    else:
        log = Log(**log_data, habit_id=int(habit_id))
        log.save()

    return log_schema.dump(log), 201


@log_router.route(f'{base_url}/logs/<log_id>', methods=['PUT'])
@jwt_required_verify_user_and_habit()
def put_log(user_id, habit_id, log_id):
    habit = Habit.find_by_id(habit_id)
    if not habit or user_id != str(habit.user_id):
        return {'message': 'Habit not found'}, 404

    log = Log.find_by_id(log_id)
    if not log or habit_id != str(log.habit_id):
        return {'message': 'Log not found'}, 404

    body = request.get_json(force=True)
    errors = log_schema.validate(body)
    if errors:
        return {
            "message": "Invalid field(s)",
            "data": errors
        }, 400

    log_data = log_schema.load(body)
    Log.update_by_id(log_id, log_data)
    updated_log = Log.find_by_id(log_id)

    return log_schema.dump(updated_log), 200
