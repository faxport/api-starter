#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools


def serialize(default):
    def decorate(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result, code, headers = func(self, *args, **kwargs)
            if code >= 400:
                return result, code, headers

            # You can assign serializer in request.
            # priority: self.serializer > serialize(default)
            _serializer = self.get_attr('serializer', None)
            serializer = _serializer or default

            # You can assign context in request.
            c = self.get_attr('context', {})
            s = serializer(many=isinstance(result, (list, tuple)))
            s.context.update(c)
            return s.dump(result).data, code, headers
        return wrapper
    return decorate
