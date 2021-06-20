"""Module for marshmallow schemas for habit"""
from marshmallow import Schema, fields, validate
from main.schemas.base import BaseSchema
from main.schemas.log import LogSchema
from main.enums import HabitStatus


class HabitSchema(BaseSchema):
    """Schema for validating habit response data"""

    name = fields.String()
    countable = fields.Boolean(dump_only=True)
    logs = fields.List(fields.Nested(LogSchema), dump_only=True)
    status = fields.String(
        load_only=True,
        validate=[validate.OneOf([HabitStatus.ACTIVE, HabitStatus.DELETED])],
    )


class PostHabitSchema(HabitSchema):
    """Schema for validating habit POST request data"""

    class Meta:
        """Options class"""

        exclude = ("status",)

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


class PutHabitSchema(HabitSchema):
    """Schema for validating habit PUT request data"""


class HabitQueryParamsSchema(Schema):
    """Schema for validating query params for GET habits (with nested logs)"""

    logyear = fields.Integer(
        required=True, error_messages={"required": "Logyear required"}
    )
    logmonth = fields.Integer(
        required=True, error_messages={"required": "Logmonth required"}
    )
    page = fields.Integer(required=True, error_messages={"required": "Page required"})


habit_schema = HabitSchema()
habits_schema = HabitSchema(many=True)
post_habit_schema = PostHabitSchema()
put_habit_schema = PutHabitSchema()
habit_query_params_schema = HabitQueryParamsSchema()
