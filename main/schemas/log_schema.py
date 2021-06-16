"""Module for marshmallow schemas for log"""
from marshmallow import Schema, fields
from main.schemas.base_schema import BaseSchema


class LogSchema(BaseSchema):
    """Schema for validating log response data and log PUT request data"""

    date = fields.Date(dump_only=True)
    count = fields.Integer(strict=True)


class NewLogSchema(Schema):
    """Schema for validating POST request data for uncountable log"""

    date = fields.Date(
        required=True, load_only=True, error_messages={"required": "Date required"}
    )


class NewLogWithCountSchema(NewLogSchema):
    """Schema for validating POST request data for countable log"""

    count = fields.Integer(
        required=True,
        strict=True,
        load_only=True,
        error_messages={"required": "Count required"},
    )


log_schema = LogSchema()
logs_schema = LogSchema(many=True)
new_log_schema = NewLogSchema()
new_log_with_count_schema = NewLogWithCountSchema()
