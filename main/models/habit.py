"""Module for Habit model"""
from main.db import db


class Habit(db.Model):
    """Habit Model for 'habits' table"""

    __tablename__ = "habits"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    countable = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<Habit(id={self.id}, name={self.name}, user_id={self.user_id}, "
            + f"countable={self.countable}, status={self.status}, "
            + f"created_at={self.created_at}, updated_at={self.updated_at})>"
        )

    @classmethod
    def get_habit_count(cls, user_id):
        """Return count of all habits owned by user"""
        return cls.query.filter_by(user_id=user_id, status="active").count()

    @classmethod
    def get_paginated(cls, user_id, *args):
        """Return a paginated list of habits"""
        habits = (
            cls.query.filter_by(user_id=user_id, status="active")
            .order_by(cls.created_at.desc())
            .paginate(*args)
            .items
        )
        return habits
