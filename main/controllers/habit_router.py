"""Module for habit_router blueprint"""
from flask import Blueprint, request
from main.models.habit import Habit
from main.models.log import Log
from main.schemas.habit_schema import (
    habit_schema, habits_schema, new_habit_schema, get_habit_query_params_schema
)
from main.utils.decorators import (
    jwt_required_verify_user, jwt_required_verify_user_and_habit
)

habit_router = Blueprint('habit_router', __name__)
base_url = '/users/<user_id>/habits'


@habit_router.route(base_url, methods=['GET'])
@jwt_required_verify_user()
def get_habits(user_id):
    errors = get_habit_query_params_schema.validate(request.args)
    if errors:
        return {
            'message': 'Invalid query parameters',
            'data': errors
        }

    query_params = get_habit_query_params_schema.load(request.args)
    habits_per_page = 20
    if not query_params['page']:
        return {'message': 'Page query parameter required'}

    habits = Habit.get_in_month_paginated(query_params['page'], habits_per_page, False)
    for habit in habits:
        habit.logs = Log.get_by_habit_in_month(
            habit.id, query_params['logyear'], query_params['logmonth']
        )

    return {
        'total_habits': Habit.get_habit_count(),
        'habits_per_page': habits_per_page,
        'habits': habits_schema.dump(habits)
    }, 200


@habit_router.route(base_url, methods=['POST'])
@jwt_required_verify_user()
def post_habit(user_id):
    body = request.get_json(force=True)
    errors = new_habit_schema.validate(body)
    if errors:
        return {
            "message": "Invalid field(s)",
            "data": errors
        }, 400

    habit_data = new_habit_schema.load(body)
    habit = Habit(**habit_data, user_id=int(user_id))
    habit.save()

    return habit_schema.dump(habit), 201


@habit_router.route(f'{base_url}/<habit_id>', methods=['PUT'])
@jwt_required_verify_user_and_habit()
def put_habit(user_id, habit_id):
    body = request.get_json(force=True)
    errors = habit_schema.validate(body)
    if errors:
        return {
            "message": "Invalid field(s)",
            "data": errors
        }, 400

    habit_data = habit_schema.load(body)
    Habit.update_by_id(habit_id, habit_data)
    updated_habit = Habit.find_by_id(habit_id)

    return habit_schema.dump(updated_habit), 200
