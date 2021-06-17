"""Module for Log model"""
from sqlalchemy import extract
from main.db import db


class Log(db.Model):
    """Log Model for 'logs' table"""

    __tablename__ = "logs"

    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    count = db.Column(db.Integer, nullable=True)  # defaults to NULL

    def __repr__(self) -> str:
        return (
            f"<Log(habit_id={self.habit_id}, date={self.date}, count={self.count}, "
            + f"id={self.id}, created_at={self.created_at}, updated_at={self.updated_at})>"
        )

    @classmethod
    def get_by_habit_in_month(cls, habit_id, year, month):
        """Return logs for the given habit_id in the given month"""
        return (
            cls.query.filter_by(habit_id=habit_id, status="active")
            .filter(extract("year", Log.date) == year)
            .filter(extract("month", Log.date) == month)
            .all()
        )

    @classmethod
    def get_one(cls, **kwargs):
        """Return a log with fields matching for the given kwargs"""
        return cls.query.filter_by(**kwargs).first()
