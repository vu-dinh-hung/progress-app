"""Module for BaseSchema"""
from marshmallow import Schema, fields


class BaseSchema(Schema):
    """BaseSchema contains base fields all other schemas should have"""

    id = fields.Integer(dump_only=True)
