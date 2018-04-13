#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import dotenv


# Load dotenv
python_env = os.getenv('PYTHON_ENV') or 'development'
dotenv_path = os.path.join(
    os.path.dirname(__file__),
    '.env.' + python_env
)
dotenv.load_dotenv(dotenv_path)


def get(key, default=None):
    return os.getenv(key) or default


def must_get(key):
    value = os.getenv(key)
    if value is None:
        raise Exception('Dotenv {} is not specified.'.format(key))
    return value


def get_int(key, default=None):
    value = get(key, default=default)
    if value is not None:
        return int(value)
    return default


def get_bool(key, default=None):
    value = get_int(key)
    if value is not None:
        return bool(value)
    return default
