"""Module for habit_router blueprint"""
# pylint: disable=unused-argument
from flask import Blueprint
from main.engines.habit import (
    update_habit,
    get_habits_paginated,
    get_habit_count,
    create_habit,
)
from main.schemas.habit import (
    habit_schema,
    habits_schema,
    post_habit_schema,
    put_habit_schema,
    habit_query_params_schema,
)
from main.engines.log import get_logs_by_habit_in_month
from main.utils.decorators import (
    load_data,
    verify_user,
    verify_habit,
)

habit_router = Blueprint("habit_router", __name__)
BASE_URL = "/users/<int:user_id>/habits"


@habit_router.route(BASE_URL, methods=["GET"])
@verify_user
@load_data(habit_query_params_schema)
def get(user_id, user, data):
    """GET habits"""
    habits_per_page = 20

    habits = get_habits_paginated(user.id, data["page"], habits_per_page, False)
    for habit in habits:
        habit.logs = get_logs_by_habit_in_month(
            habit.id, data["logyear"], data["logmonth"]
        )

    return {
        "total_habits": get_habit_count(user.id),
        "habits_per_page": habits_per_page,
        "habits": habits_schema.dump(habits),
    }, 200


@habit_router.route(BASE_URL, methods=["POST"])
@verify_user
@load_data(post_habit_schema)
def post(user_id, user, data):
    """POST habit"""
    habit = create_habit(**data, user_id=user.id)

    return habit_schema.dump(habit), 201


@habit_router.route(f"{BASE_URL}/<int:habit_id>", methods=["PUT"])
@verify_user
@verify_habit
@load_data(put_habit_schema)
def put(user_id, habit_id, user, habit, data):
    """PUT habit"""
    updated_habit = update_habit(habit, data)

    return habit_schema.dump(updated_habit), 200
