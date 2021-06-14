"""Module for initializing the SQLAlchemy object"""
from datetime import datetime
from contextlib import contextmanager
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import validates
from marshmallow import Schema, fields, validate


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

    @classmethod
    def find_by_id(cls, _id):
        """Return the resource with the given id
        or None if the id does not exist"""
        return cls.query.get(_id)

    @classmethod
    def update_by_id(cls, _id, data_dict):
        """Update the resource with the given id using data_dict"""
        with session_scope() as session:
            session.query(cls).filter_by(id=_id).update(data_dict)

    def save(self):
        """Add/update this resource in the database"""
        with session_scope() as session:
            db.session.add(self)


class BaseSchema(Schema):
    id = fields.Int(dump_only=True)
    status = fields.String(load_only=True, validate=[validate.OneOf(('active', 'deleted'))])


db = SQLAlchemy(model_class=Base)
