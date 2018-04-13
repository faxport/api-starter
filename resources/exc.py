#!/usr/bin/env python
# -*- coding: utf-8 -*-


class RequestError(Exception):

    def __init__(self, code=422, message=None, error=None,
                 errors=None, headers=None):
        super().__init__(message)
        self.message = message
        self.error = error
        self.errors = errors
        self.headers = headers
        self.code = code
