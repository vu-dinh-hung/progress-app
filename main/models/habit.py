"""Module for Habit model"""
from main.db import db, session_scope
from sqlalchemy.orm import validates


class Habit(db.Model):
    """Habit Model for 'habits' table"""
    __tablename__ = 'habits'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    countable = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f'<Habit(name={self.name}, user_id={self.user_id}, countable={self.countable}, ' +\
            f'id={self.id}, created_at={self.created_at}, updated_at={self.updated_at})>'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Habit): return False
        if self.id != o.id: return False
        if self.user_id != o.user_id: return False
        if self.name != o.name: return False
        if self.countable != o.countable: return False
        return True

    @validates('countable')
    def validate_updated_at(self, key, value):
        if self.countable:
            raise ValueError('Cannot update countable')
        return value

    def to_dict(self) -> dict:
        """Return the dictionary representation of this habit"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'countable': self.countable
        }

    @classmethod
    def find_by_id(cls, habit_id):
        """Return the habit with the given id
        or None if the id does not exist"""
        return cls.query.get(habit_id)

    def save(self):
        """Add/update this habit in the database"""
        with session_scope() as session:
            db.session.add(self)
