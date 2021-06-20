"""Module for log_router blueprint"""
# pylint: disable=unused-argument
from flask import Blueprint
from main.models.user import User
from main.models.habit import Habit
from main.models.log import Log
from main.engines.log import update_log, create_log
from main.schemas.log import log_schema, post_log_schema, put_log_schema
from main.utils.decorators import load_data, verify_user, verify_habit, verify_log

log_router = Blueprint("log_router", __name__)
BASE_URL = "/users/<int:user_id>/habits/<int:habit_id>"


@log_router.route(f"{BASE_URL}/logs", methods=["POST"])
@verify_user
@verify_habit
@load_data(post_log_schema)
def post(user_id: int, habit_id: int, user: User, habit: Habit, data: dict):
    """POST log"""
    log = create_log(**data, habit_id=habit.id)

    return log_schema.dump(log), 201


@log_router.route(f"{BASE_URL}/logs/<int:log_id>", methods=["PUT"])
@verify_user
@verify_habit
@verify_log
@load_data(put_log_schema)
def put(
    user_id: int,
    habit_id: int,
    log_id: int,
    user: User,
    habit: Habit,
    log: Log,
    data: dict,
):
    """PUT log"""
    updated_log = update_log(log, data)

    return log_schema.dump(updated_log), 200
