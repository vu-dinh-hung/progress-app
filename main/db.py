"""Module for initializing the SQLAlchemy object"""
from datetime import datetime
from contextlib import contextmanager
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import validates
from marshmallow import Schema, fields, validate


class Base(Model):
    """Base class for all Models"""
    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = sa.Column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    status = sa.Column(sa.String(32), default='active', nullable=False)

    @validates('id')
    def validate_id(self, key, value):
        if self.id:
            raise ValueError('Cannot update id')
        return value

    @validates('created_at')
    def validate_created_at(self, key, value):
        if self.created_at:
            raise ValueError('Cannot update created_at')
        return value

    @validates('updated_at')
    def validate_updated_at(self, key, value):
        if self.updated_at:
            raise ValueError('Cannot update created_at')
        return value


class BaseSchema(Schema):
    id = fields.Int(dump_only=True)
    status = fields.String(load_only=True, validate=[validate.OneOf(('active', 'deleted'))])


@contextmanager
def session_scope():
    """Provide a transactional scope"""
    session = db.session
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise


db = SQLAlchemy(model_class=Base)
