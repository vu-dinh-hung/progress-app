"""Module for habit_router blueprint"""
from flask import Blueprint
from main.engines.habit import HabitEngine
from main.engines.log import LogEngine
from main.schemas.habit import (
    habit_schema,
    habits_schema,
    new_habit_schema,
    habit_query_params_schema,
)
from main.utils.decorators import (
    load_body,
    verify_user,
    verify_habit,
)

habit_router = Blueprint("habit_router", __name__)
BASE_URL = "/users/<int:user_id>/habits"


@habit_router.route(BASE_URL, methods=["GET"])
@verify_user
@load_body(habit_query_params_schema)
def get_habits(user_id, data):
    """GET habits"""
    habits_per_page = 20

    habits = HabitEngine.get_habits_paginated(
        user_id, data["page"], habits_per_page, False
    )
    for habit in habits:
        habit.logs = LogEngine.get_logs_by_habit_in_month(
            habit.id, data["logyear"], data["logmonth"]
        )

    return {
        "total_habits": HabitEngine.get_habit_count(user_id),
        "habits_per_page": habits_per_page,
        "habits": habits_schema.dump(habits),
    }, 200


@habit_router.route(BASE_URL, methods=["POST"])
@verify_user
@load_body(new_habit_schema)
def post_habit(data, user_id):
    """POST habit"""
    habit = HabitEngine.create_habit(**data, user_id=int(user_id))

    return habit_schema.dump(habit), 201


@habit_router.route(f"{BASE_URL}/<int:habit_id>", methods=["PUT"])
@load_body(habit_schema)
@verify_habit
@verify_user
def put_habit(data, user_id, habit_id):  # pylint: disable=unused-argument
    """PUT habit"""
    HabitEngine.update_by_id(habit_id, data)
    updated_habit = HabitEngine.find_by_id(habit_id)

    return habit_schema.dump(updated_habit), 200
