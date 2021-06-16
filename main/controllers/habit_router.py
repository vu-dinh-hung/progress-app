"""Module for habit_router blueprint"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.models.habit import Habit
from main.models.log import Log
from main.schemas.habit_schema import (
    habit_schema, habits_schema, new_habit_schema, get_habit_query_params_schema
)

habit_router = Blueprint('habit_router', __name__)
base_url = '/users/<user_id>/habits'


@habit_router.route(base_url, methods=['GET'])
@jwt_required()
def get_habits(user_id):
    jwt_id = get_jwt_identity()
    if user_id != str(jwt_id):
        return {'message': 'User not found'}, 404

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
@jwt_required()
def post_habit(user_id):
    jwt_id = get_jwt_identity()
    if user_id != str(jwt_id):
        return {'message': 'User not found'}, 404

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
@jwt_required()
def put_habit(user_id, habit_id):
    jwt_id = get_jwt_identity()
    if user_id != str(jwt_id):
        return {'message': 'User not found'}, 404

    habit = Habit.find_by_id(habit_id)
    if not habit or user_id != str(habit.user_id):
        return {'message': 'Habit not found'}, 404

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
