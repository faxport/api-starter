#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import os

import utils


def authorize(func=None):
    def decorate(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            _authorize(self, account=self.current_account)
            return func(self, *args, **kwargs)
        return wrapper
    if func:
        return decorate(func)
    return decorate


def _authorize(req, account=None):
    if not account:
        req.raise_exc(code=401, message='Invalid authorization')
