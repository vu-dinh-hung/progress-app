"""Module for User model"""
from main.db import db


class User(db.Model):
    """User Model for 'users' table"""

    __tablename__ = "users"

    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(50), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, username={self.username}, name={self.name}, "
            + f"created_at={self.created_at}, updated_at={self.updated_at})>"
        )
