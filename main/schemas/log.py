"""Module for marshmallow schemas for log"""
from marshmallow import fields, validate
from main.schemas.base import BaseSchema
from main.enums import LogStatus


class LogSchema(BaseSchema):
    """Schema for validating log response data"""

    date = fields.Date(dump_only=True)
    count = fields.Integer(strict=True)
    status = fields.String(
        load_only=True,
        validate=[validate.OneOf([LogStatus.ACTIVE, LogStatus.DELETED])],
    )


class PostLogSchema(LogSchema):
    """Schema for validating log POST request data"""

    class Meta:
        """Options class"""

        exclude = ("status",)

    count = fields.Integer(
        strict=True,
        load_only=True,
        error_messages={"required": "Count required"},
    )

    date = fields.Date(
        required=True, load_only=True, error_messages={"required": "Date required"}
    )


class PutLogSchema(LogSchema):
    """Schema for validating log PUT request data"""


log_schema = LogSchema()
logs_schema = LogSchema(many=True)
post_log_schema = PostLogSchema()
put_log_schema = PutLogSchema()
