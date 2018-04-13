#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import time

import sqlalchemy as sa

import models


def capture_exc(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        import resources
        try:
            result = func(self, *args, **kwargs)
            return result
        except models.exc.ModelError as e:
            return _errorify(message=e.message, errors=e.errors, code=e.code)
        except sa.exc.IntegrityError as e:
            return _errorify(message='Record exists, do not do over again', error=str(e))
        except sa.exc.SQLAlchemyError as e:
            import traceback
            traceback.print_exc()
            return _errorify(message='Internal server error, please contact the administrator', error=str(e), code=500)
        except resources.exc.RequestError as e:
            return _errorify(message=e.message, errors=e.errors, code=e.code, headers=e.headers)
    return wrapper


def _errorify(code=422, message=None, error=None, errors=None, headers=None):
    result = {
        'errcode': code,
        'message': message or 'Request failed, please try again later',
    }
    if error:
        result['error'] = error
    if errors:
        result['errors'] = errors

    return result, code, headers or {}
