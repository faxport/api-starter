#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ModelError(Exception):

    def __init__(self, message, errors=None, code=None):
        super().__init__(message)
        self.message = message
        self.errors = errors
        self.code = code
