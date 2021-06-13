"""Module for Log model"""
from main.db import db, session_scope
from sqlalchemy.orm import validates


class Log(db.Model):
    """Log Model for 'logs' table"""
    __tablename__ = 'logs'

    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    count = db.Column(db.Integer, nullable=True)  # defaults to NULL

    def __repr__(self) -> str:
        return f'<Log(habit_id={self.habit_id}, date={self.date}, count={self.count}, ' +\
            f'id={self.id}, created_at={self.created_at}, updated_at={self.updated_at})>'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Log): return False
        if self.id != o.id: return False
        if self.habit_id != o.habit_id: return False
        if self.date != o.date: return False
        if self.count != o.count: return False
        return True

    @validates('date')
    def validate_updated_at(self, key, value):
        if self.date:
            raise ValueError('Cannot update date')
        return value

    def to_dict(self) -> dict:
        """Return the dictionary representation of this log"""
        return {
            'id': self.id,
            'habit_id': self.habit_id,
            'date': self.date.isoformat(),
            'count': self.count
        }

    @classmethod
    def find_by_id(cls, log_id):
        """Return the log with the given id
        or None if the id does not exist"""
        return cls.query.get(log_id)

    def save(self):
        """Add/update this log in the database"""
        with session_scope() as session:
            db.session.add(self)
