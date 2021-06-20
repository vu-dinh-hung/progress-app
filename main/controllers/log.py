"""Module for log_router blueprint"""
from flask import Blueprint, request
from main.engines.habit import HabitEngine
from main.engines.log import LogEngine
from main.schemas.log import (
    log_schema,
    new_log_schema,
    new_log_with_count_schema,
)
from main.utils.decorators import load_data, verify_user, verify_habit
from main.enums import LogStatus
from main.exceptions import BadRequestError, NotFoundError

log_router = Blueprint("log_router", __name__)
BASE_URL = "/users/<int:user_id>/habits/<int:habit_id>"


@log_router.route(f"{BASE_URL}/logs", methods=["POST"])
@verify_habit
@verify_user
def post_log(user_id, habit_id):  # pylint: disable=unused-argument
    """POST log"""
    habit = HabitEngine.find_by_id(habit_id)

    # load log schema according to countability of habit
    schema = new_log_with_count_schema if habit.countable else new_log_schema

    body = request.get_json(force=True)
    errors = schema.validate(body)
    if errors:
        raise BadRequestError("Invalid field(s)", errors)

    log_data = schema.load(body)

    # if log for given date and habit already exists, set status of that log to 'active'
    log_in_db = LogEngine.get_log_by_habit_and_date(habit_id, log_data["date"])
    log = None
    if log_in_db:
        log_in_db.status = LogStatus.ACTIVE
        log_in_db.save()
        log = log_in_db
    else:
        log = LogEngine.create_log(**log_data, habit_id=int(habit_id))

    return log_schema.dump(log), 201


@log_router.route(f"{BASE_URL}/logs/<int:log_id>", methods=["PUT"])
@verify_habit
@verify_user
@load_data(log_schema)
def put_log(data, user_id, habit_id, log_id):  # pylint: disable=unused-argument
    """PUT log"""
    log = LogEngine.find_by_id(log_id)
    if not log or habit_id != log.habit_id:
        raise NotFoundError("Log not found")

    LogEngine.update_by_id(log_id, data)
    updated_log = LogEngine.find_by_id(log_id)

    return log_schema.dump(updated_log), 200
