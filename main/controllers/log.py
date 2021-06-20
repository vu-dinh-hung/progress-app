"""Module for log_router blueprint"""
# pylint: disable=unused-argument
from flask import Blueprint, request
from main.engines.log import get_log, update_log, create_log
from main.schemas.log import (
    log_schema,
    new_log_schema,
    new_log_with_count_schema,
)
from main.utils.decorators import load_data, verify_user, verify_habit, verify_log
from main.exceptions import BadRequestError

log_router = Blueprint("log_router", __name__)
BASE_URL = "/users/<int:user_id>/habits/<int:habit_id>"


@log_router.route(f"{BASE_URL}/logs", methods=["POST"])
@verify_user
@verify_habit
def post(user_id, habit_id, user, habit):
    """POST log"""
    # load log schema according to countability of habit
    schema = new_log_with_count_schema if habit.countable else new_log_schema

    body = request.get_json(force=True)
    errors = schema.validate(body)
    if errors:
        raise BadRequestError("Invalid field(s)", errors)

    log_data = schema.load(body)

    log = create_log(**log_data, habit_id=habit.id)

    return log_schema.dump(log), 201


@log_router.route(f"{BASE_URL}/logs/<int:log_id>", methods=["PUT"])
@verify_user
@verify_habit
@verify_log
@load_data(log_schema)
def put(
    user_id, habit_id, log_id, user, habit, log, data
):  # pylint: disable=unused-argument
    """PUT log"""
    update_log(log.id, data)
    updated_log = get_log(log.id)

    return log_schema.dump(updated_log), 200
