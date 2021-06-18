"""Module for Log model"""
from main.db import db
from main.enums import LogStatus


class Log(db.Model):
    """Log Model for 'logs' table"""

    __tablename__ = "logs"

    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    count = db.Column(db.Integer, nullable=True)  # defaults to NULL
    status = db.Column(db.String(32), default=LogStatus.ACTIVE.value, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<Log(habit_id={self.habit_id}, date={self.date}, count={self.count}, "
            + f"id={self.id}, created_at={self.created_at}, updated_at={self.updated_at})>"
        )
