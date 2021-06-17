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
