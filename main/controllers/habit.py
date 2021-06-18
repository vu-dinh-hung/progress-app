"""Module for habit_router blueprint"""
from flask import Blueprint, request
from main.engines.habit import HabitEngine
from main.engines.log import LogEngine
from main.schemas.habit import (
    habit_schema,
    habits_schema,
    new_habit_schema,
    get_habit_query_params_schema,
)
from main.utils.decorators import (
    jwt_required_verify_user,
    jwt_required_verify_user_and_habit,
)
from main.exceptions import BadRequestError

habit_router = Blueprint("habit_router", __name__)
BASE_URL = "/users/<int:user_id>/habits"


@habit_router.route(BASE_URL, methods=["GET"])
@jwt_required_verify_user()
def get_habits(user_id):
    """GET habits"""
    errors = get_habit_query_params_schema.validate(request.args)
    if errors:
        raise BadRequestError("Invalid query parameters", errors)

    query_params = get_habit_query_params_schema.load(request.args)
    habits_per_page = 20

    habits = HabitEngine.get_habits_paginated(
        user_id, query_params["page"], habits_per_page, False
    )
    for habit in habits:
        habit.logs = LogEngine.get_logs_by_habit_in_month(
            habit.id, query_params["logyear"], query_params["logmonth"]
        )

    return {
        "total_habits": HabitEngine.get_habit_count(user_id),
        "habits_per_page": habits_per_page,
        "habits": habits_schema.dump(habits),
    }, 200


@habit_router.route(BASE_URL, methods=["POST"])
@jwt_required_verify_user()
def post_habit(user_id):
    """POST habit"""
    body = request.get_json(force=True)
    errors = new_habit_schema.validate(body)
    if errors:
        raise BadRequestError("Invalid field(s)", errors)

    habit_data = new_habit_schema.load(body)
    habit = HabitEngine.create_habit(**habit_data, user_id=int(user_id))

    return habit_schema.dump(habit), 201


@habit_router.route(f"{BASE_URL}/<int:habit_id>", methods=["PUT"])
@jwt_required_verify_user_and_habit()
def put_habit(user_id, habit_id):  # pylint: disable=unused-argument
    """PUT habit"""
    body = request.get_json(force=True)
    errors = habit_schema.validate(body)
    if errors:
        raise BadRequestError("Invalid field(s)", errors)

    habit_data = habit_schema.load(body)
    HabitEngine.update_by_id(habit_id, habit_data)
    updated_habit = HabitEngine.find_by_id(habit_id)

    return habit_schema.dump(updated_habit), 200
