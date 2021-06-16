"""Module for Habit model"""
from sqlalchemy.orm import validates
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
        return cls.query.filter_by(user_id=user_id).count()

    @classmethod
    def get_in_month_paginated(cls, *args):
        """Return a paginated list of habits, with nested logs filtered by the given month"""
        habits = (
            cls.query.filter_by(status="active")
            .order_by(cls.created_at.desc())
            .paginate(*args)
            .items
        )
        return habits

    @validates("countable")
    def validate_countable(self, key, value):
        """SQLAlchemy validator for countable field"""
        if self.countable:
            raise ValueError("Cannot update field: countable")
        return value
