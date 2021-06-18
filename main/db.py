"""Module for initializing the SQLAlchemy object"""
from datetime import datetime
from contextlib import contextmanager
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import DATETIME


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
    created_at = sa.Column(DATETIME(fsp=6), default=datetime.utcnow, nullable=False)
    updated_at = sa.Column(
        DATETIME(fsp=6),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    @classmethod
    def find_by_id(cls, _id):
        """Return the resource with the given id
        or None if the id doesn't exist"""
        return cls.query.get(_id)

    @classmethod
    def update_by_id(cls, _id, data_dict):
        """Update the resource with the given id using data_dict"""
        with session_scope() as session:
            session.query(cls).filter_by(id=_id).update(data_dict)

    def save(self):
        """Add/update this resource in the database"""
        with session_scope() as session:
            session.add(self)


db = SQLAlchemy(model_class=Base)
