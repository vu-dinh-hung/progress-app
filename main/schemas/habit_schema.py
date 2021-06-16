"""Module for marshmallow schemas for habit"""
from marshmallow import Schema, fields, validate
from main.schemas.base_schema import BaseSchema
from main.schemas.log_schema import LogSchema


class HabitSchema(BaseSchema):
    """Schema for validating habit response data and habit PUT request data"""

    name = fields.String()
    countable = fields.Boolean(dump_only=True)
    logs = fields.List(fields.Nested(LogSchema), dump_only=True)


class NewHabitSchema(Schema):
    """Schema for validating habit POST request data"""

    min_name, max_name = 1, 80
    name = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=min_name,
                max=max_name,
                error=f"Habit name should be between {min_name} and {max_name} characters",
            )
        ],
        error_messages={"required": "Habit name required"},
    )
    countable = fields.Boolean()


class GetHabitQueryParamsSchema(Schema):
    """Schema for validating and constructing data for GET habits (with nested logs)"""

    logyear = fields.Integer(
        required=True, error_messages={"required": "Logyear required"}
    )
    logmonth = fields.Integer(
        required=True, error_messages={"required": "Logmonth required"}
    )
    page = fields.Integer(required=True, error_messages={"required": "Page required"})


habit_schema = HabitSchema()
habits_schema = HabitSchema(many=True)
new_habit_schema = NewHabitSchema()
get_habit_query_params_schema = GetHabitQueryParamsSchema()
