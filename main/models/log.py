"""Module for Log model"""
from sqlalchemy.orm import validates
from marshmallow import Schema, fields
from main.db import db, BaseSchema


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

    @classmethod
    def get_one(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @validates('date')
    def validate_updated_at(self, key, value):
        if self.date:
            raise ValueError('Cannot update date')
        return value


class LogSchema(BaseSchema):
    date = fields.Date(dump_only=True)
    count = fields.Integer(strict=True)


class NewLogSchema(Schema):
    date = fields.Date(
        required=True,
        load_only=True,
        error_messages={'required': {'message': 'Habit name required'}}
    )


class NewLogWithCountSchema(NewLogSchema):
    count = fields.Integer(strict=True, load_only=True)


log_schema = LogSchema()
logs_schema = LogSchema(many=True)
new_log_schema = NewLogSchema()
new_log_with_count_schema = NewLogWithCountSchema()
