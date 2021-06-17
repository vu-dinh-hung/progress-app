"""Module for LogEngine"""
from sqlalchemy import extract
from main.models.log import Log


class LogEngine:
    """Engine class for providing log-related operations"""

    @staticmethod
    def find_by_id(*args, **kwargs):
        """Return a log by id or None if log not found"""
        return Log.find_by_id(*args, **kwargs)

    @staticmethod
    def update_by_id(*args, **kwargs):
        """Update a log by id"""
        Log.update_by_id(*args, **kwargs)

    @staticmethod
    def create_log(*args, **kwargs):
        """Create and save a log into database, then return the log"""
        log = Log(*args, **kwargs)
        log.save()
        return log

    @staticmethod
    def query_logs_by_habit_id(habit_id):
        """Return a logs query object after filtering logs by habit_id and status='active'"""
        return Log.query.filter_by(habit_id=habit_id, status="active")

    @classmethod
    def get_logs_by_habit_in_month(cls, habit_id, year, month):
        """Return logs for the given habit_id in the given month"""
        return (
            cls.query_logs_by_habit_id(habit_id)
            .filter(extract("year", Log.date) == year)
            .filter(extract("month", Log.date) == month)
            .all()
        )

    @staticmethod
    def get_log_by_habit_and_date(habit_id, date):
        """Return a log that matches the given habit_id & date or None if there is no match"""
        return Log.query.filter_by(habit_id=habit_id, date=date).first()
