"""Module for BaseSchema"""
from marshmallow import Schema, fields, validate


class BaseSchema(Schema):
    """BaseSchema contains base fields all other resources should have"""

    id = fields.Int(dump_only=True)
    status = fields.String(
        load_only=True, validate=[validate.OneOf(("active", "deleted"))]
    )
