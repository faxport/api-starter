#!/usr/bin/env python
# -*- coding: utf-8 -*-

import marshmallow as ms

import const
from . import validators

__all__ = [
    'ms',
    'validators',
    'BaseSchema',
    'QuerySchema',
    'IDSchema',
    'EmptySchema',
]


class QuerySchema(ms.Schema):
    page = ms.fields.Integer(
        missing=1,
        validate=validators.page,
    )
    per_page = ms.fields.Integer(
        missing=15,
        validate=validators.per_page,
    )
    q = ms.fields.Str()


class BaseSchema(ms.Schema):
    pass


class EmptySchema(BaseSchema):
    pass


class IDSchema(BaseSchema):
    id = ms.fields.Str(
        required=True,
        error_messages={
            'required': 'ID required',
            'null': 'ID required'
        }
    )
