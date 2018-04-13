#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import re

import flask_sqlalchemy as fsa
import sqlalchemy as sa

import const
from extensions import db
from extensions import r
import utils


current_timestamp_func = lambda: datetime.datetime.utcnow().timestamp()



class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String, default=utils.url62.url62, primary_key=True)
    deleted_at = db.Column(db.Float)
    created_at = db.Column(db.Float, default=current_timestamp_func)
    updated_at = db.Column(db.Float, default=current_timestamp_func, onupdate=current_timestamp_func)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)

    @classmethod
    def raise_exc(cls, message, errors=None, code=422, field=None):
        if field:
            errors = errors or {}
            errors[field] = [message]
        # NOTE: Add rollback before raising exc
        db.session.rollback()
        raise exc.ModelError(message=message, errors=errors, code=code)

    @classmethod
    def find_by_id(cls, id, field='id'):
        return cls.find_one_by(**{field: id})

    @classmethod
    def find_one_by(cls, **criteria):
        query = cls.init_query(**criteria)
        return query.first()

    @classmethod
    def find_by(cls, **criteria):
        query = cls.init_query(**criteria)
        return query

    @classmethod
    def add(cls, **kwargs):
        self = cls()
        return self.update(**kwargs)

    def save(self):
        return self.commit(self)

    def update(self, **kwargs):
        self._set_fields(kwargs)
        return self.commit(self)

    def reload(self):
        record = self.find_by_id(self.id)
        if not record:
            self.raise_exc('Record not found with id={}'.format(self.id), code=404)
        for i in record.__table__.columns:
            setattr(self, i.name, getattr(record, i.name))

    def delete(self):
        self.commit(self, delete=True)

    def soft_delete(self):
        self.deleted_at = datetime.datetime.utcnow().timestamp()
        self.commit(self)

    @classmethod
    def delete_by(cls, **criteria):
        query = cls.init_query(**criteria)
        cls.commit(query.all(), delete=True)

    @classmethod
    def soft_delete_by(cls, **criteria):
        query = cls.init_query(**criteria)
        os = []
        deleted_at = datetime.datetime.utcnow().timestamp()
        for o in query:
            o.deleted_at = deleted_at
            os.append(o)
        cls.commit(os)

    @classmethod
    def init_query(cls, **criteria):
        query = cls.query.filter_by(**criteria)
        query = cls.without_deleted(query)
        query = query.order_by(cls.created_at.desc())
        return query

    @classmethod
    def paginate(cls, query, page=1, per_page=15):
        total = query.count()
        query = query.offset((page - 1) * per_page).limit(per_page)
        return query.all(), total

    @classmethod
    def without_deleted(cls, query=None):
        query = query or cls.query
        query = query.filter(cls.deleted_at.is_(None))
        return query

    def _set_fields(self, kwargs):
        # NOTE: Use _set_fields for add/update operation.
        for k, v in kwargs.items():
            # NOTE: Add `_set_fields_for_{field}` to customize set value.
            func = getattr(self, '_set_fields_for_{}'.format(k), None)
            if func and callable(func):
                func(kwargs)
            else:
                setattr(self, k, v)

    def _commit():
        try:
            db.session.commit()
        except sa.exc.SQLAlchemyError as e:
            import traceback
            traceback.print_exc()
            db.session.rollback()
            raise e

    @classmethod
    def commit(cls, obj=None, delete=False):
        if not obj:
            return

        # delete obj
        if delete is True:
            if isinstance(obj, list):
                for o in obj:
                    db.session.delete(o)
                    cls._commit()
            else:
                db.session.delete(obj)
                cls._commit()

        # add obj
        if delete is False:
            if isinstance(obj, list):
                db.session.add_all(obj)
                cls._commit()
            else:
                db.session.add(obj)
                cls._commit()

        return obj
