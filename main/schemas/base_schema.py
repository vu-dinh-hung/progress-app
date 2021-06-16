from marshmallow import Schema, fields, validate


class BaseSchema(Schema):
    id = fields.Int(dump_only=True)
    status = fields.String(load_only=True, validate=[validate.OneOf(('active', 'deleted'))])
