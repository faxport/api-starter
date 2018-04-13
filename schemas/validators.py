#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import re

import arrow
import marshmallow as ms


def int_range(value, min_value=None, max_value=None):
    try:
        x = int(value)
    except ValueError:
        raise ms.ValidationError('Must be integer')
    if min_value is not None and x < min_value:
        raise ms.ValidationError('Must not be smaller than {}'.format(min_value))
    if max_value is not None and x > max_value:
        raise ms.ValidationError('Must not be bigger than {}'.format(max_value))
    return x


page = functools.partial(int_range, min_value=1)
per_page = functools.partial(int_range, min_value=1, max_value=100)


def integer(value):
    if value == "":
        return value
    if isinstance(value, float):
        return False
    if isinstance(value, str):
        pattern = u'^\d{1,}$'
        if not re.match(pattern, value):
            return False
    return value


def iso8601(value):
    try:
        return arrow.get(value).datetime.replace(tzinfo=None)
    except Exception:
        raise ms.ValidationError('Invalid ISO8601 format')


def email(value):
    if value == "":
        return value
    pattern = u'^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
    if not re.match(pattern, value):
        raise ms.ValidationError('Invalid email')
    return value


def url(value):
    if value == "":
        return value
    pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    if not re.match(pattern, value):
        raise ms.ValidationError('Invalid URL')
    return value


def password(value):
    if len(value) < 8 or len(value) > 32:
        raise ms.ValidationError('Password should be 8-32 characters')
    pattern = r'^[0-9a-zA-Z!"#\$%&\'()*+,-\./:;<=>?@[\\\]^_`{|}~]{8,32}$'
    if not re.match(pattern, value):
        raise ms.ValidationError('Password should not contain special characters')
    return value


def string(value, min_len=2, max_len=32, msg=None):
    if value == "":
        return value
    pattern = u'^.{' + str(min_len) + ',' + str(max_len) + '}$'
    if not re.match(pattern, value, re.DOTALL):
        if msg:
            raise ms.ValidationError(msg)
        return False
    return value
