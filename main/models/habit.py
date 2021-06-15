"""Module for Habit model"""
from sqlalchemy.orm import validates
from marshmallow import Schema, fields, validate
from main.db import db, BaseSchema
from main.models.log import LogSchema


class Habit(db.Model):
    """Habit Model for 'habits' table"""
    __tablename__ = 'habits'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    countable = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f'<Habit(id={self.id}, name={self.name}, user_id={self.user_id}, ' +\
            f'countable={self.countable}, status={self.status}, ' +\
            f'created_at={self.created_at}, updated_at={self.updated_at})>'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Habit): return False
        if self.id != o.id: return False
        if self.user_id != o.user_id: return False
        if self.name != o.name: return False
        if self.countable != o.countable: return False
        return True

    @classmethod
    def get_habit_count(cls):
        return cls.query.count()

    @classmethod
    def get_in_month_paginated(cls, *args):
        habits = cls.query.filter_by(status='active').\
            order_by(cls.created_at.desc()).paginate(*args).items
        return habits

    @validates('countable')
    def validate_countable(self, key, value):
        if self.countable:
            raise ValueError('Cannot update countable')
        return value


class HabitSchema(BaseSchema):
    name = fields.String()
    countable = fields.Boolean(dump_only=True)
    logs = fields.List(fields.Nested(LogSchema), dump_only=True)


class NewHabitSchema(Schema):
    min_name, max_name = 1, 80
    name = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=min_name, max=max_name,
                error=f'Habit name should be between {min_name} and {max_name} characters'
            )
        ],
        error_messages={'required': {'message': 'Habit name required'}}
    )
    countable = fields.Boolean()


class GetHabitQueryParamsSchema(Schema):
    logyear = fields.Integer(
        required=True,
        error_messages={'required': {'message': 'Logyear required'}}
    )
    logmonth = fields.Integer(
        required=True,
        error_messages={'required': {'message': 'Logmonth required'}}
    )
    page = fields.Integer(
        required=True,
        error_messages={'required': {'message': 'Page required'}}
    )



habit_schema = HabitSchema()
habits_schema = HabitSchema(many=True)
new_habit_schema = NewHabitSchema()
get_habit_query_params_schema = GetHabitQueryParamsSchema()
