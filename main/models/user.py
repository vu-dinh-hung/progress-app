"""Module for User model"""
import bcrypt
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
            + f"status={self.status}, created_at={self.created_at}, updated_at={self.updated_at})>"
        )

    @classmethod
    def find_by_username(cls, username):
        """Return the user with the given username
        or None if the username does not exist
        """
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def hash_password(password):
        """Return a secure hash for the given password"""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(14))

    def check_password(self, password):
        """Compare the given password with the user's password_hash"""
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )
