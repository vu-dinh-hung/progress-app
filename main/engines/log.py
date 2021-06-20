"""Module for log-related operations"""
from typing import Optional, List
import datetime
from sqlalchemy import extract
from main.models.log import Log
from main.enums import LogStatus
from main.exceptions import BadRequestError
from main.engines.habit import get_habit


def get_log(log_id: int) -> Optional[Log]:
    """Return a log by id or None if log not found"""
    return Log.find_by_id(log_id)


def update_log(log: Log, data: dict) -> Log:
    """Update a log by id"""
    Log.update_by_id(log.id, data)
    return Log.find_by_id(log.id)


def create_log(
    *, habit_id: int, date: datetime.date, count: Optional[int] = None
) -> Log:
    """Create and save a log into database, then return the log"""
    # Verify 'count' field
    habit = get_habit(habit_id)
    if habit.countable and count is None:
        raise BadRequestError("Log for countable habit should include a count")

    if not habit.countable and count is not None:
        raise BadRequestError("Log for uncountable habit should not include a count")

    # If log for given date and habit already exists, set status of that log to 'active'
    log = get_log_by_habit_and_date(habit_id, date)
    if log:
        log.status = LogStatus.ACTIVE
        log.save()
    else:
        log = Log(habit_id=habit_id, date=date, count=count)
        log.save()

    return log


def query_logs_by_habit_id(habit_id: int):
    """Return a logs query object after filtering logs by habit_id and status='active'"""
    return Log.query.filter_by(habit_id=habit_id, status=LogStatus.ACTIVE)


def get_logs_by_habit_in_month(habit_id: int, logyear: int, logmonth: int) -> List[Log]:
    """Return logs for the given habit_id in the given month"""
    return (
        query_logs_by_habit_id(habit_id)
        .filter(extract("year", Log.date) == logyear)
        .filter(extract("month", Log.date) == logmonth)
        .all()
    )


def get_log_by_habit_and_date(habit_id: int, date: datetime.date) -> Optional[Log]:
    """Return a log that matches the given habit_id & date or None if there is no match"""
    return Log.query.filter_by(habit_id=habit_id, date=date).first()
