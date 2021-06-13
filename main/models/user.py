"""Module for User model"""
from main.db import db, session_scope


class User(db.Model):
    """User Model for 'users' table"""
    __tablename__ = 'users'

    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(50), nullable=True)

    def __repr__(self) -> str:
        return f'<User(username={self.username}, name={self.name}, ' +\
            f'id={self.id}, created_at={self.created_at}, updated_at={self.updated_at})>'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, User): return False
        if self.id != o.id: return False
        if self.username != o.username: return False
        if self.name != o.name: return False
        if self.password_hash != o.password_hash: return False
        return True

    def to_dict(self) -> dict:
        """Return the dictionary representation of this user"""
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name
        }

    @classmethod
    def find_by_id(cls, user_id):
        """Return the user with the given id or None if the id does not exist"""
        return cls.query.get(user_id)

    @classmethod
    def find_by_username(cls, username):
        """Return the user with the given username
        or None if the username does not exist
        """
        return cls.query.filter_by(username=username).first()

    def save(self):
        """Add/update this user in the database"""
        with session_scope() as session:
            db.session.add(self)
