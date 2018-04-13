#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
from flask import request


def _errors_unify(errors):
    """
    FIXME:if the input data structure is more complicated, like:
    {
        'address':[
            {'country':'US'},
            {'city':'New York City'}
        ]
    }
    here we still haven't resolved this case in validator yet.
    """
    for field, error_messages in errors.items():
        if isinstance(error_messages, dict):
            nested = []
            for values in error_messages.values():
                nested.extend(values)
            errors[field] = list(set(nested))
    return errors


def _validated_data(req, method, schema, data, partial=None, ctx=None):
    # BUG: Schema.load method don't check None
    # Ref:https://github.com/marshmallow-code/marshmallow/issues/511
    s = schema()
    s.context.update(ctx or {})
    result, errors = s.load(data, partial=partial)
    if errors:
        errors = _errors_unify(errors)
        code = 400 if method in ['GET'] else 422
        req.raise_exc(code=code, message='Input faileds invalid', errors=errors)
    return result


def validate(schema, partial=None):
    def decorate(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            method = request.method
            if method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                data = request.get_json(force=True, silent=True) or {}
                body = _validated_data(self, method, schema, data, partial)
                self.body = body
            if method in ['GET']:
                data = request.args
                self.args = _validated_data(self, method, schema, data, partial)
            return func(self, *args, **kwargs)
        return wrapper
    return decorate
