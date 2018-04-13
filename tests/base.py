#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from http import HTTPStatus as h
import json as j
import random
from unittest import mock
import uuid


from flask_testing import TestCase

import app
from extensions import db
from extensions import r
import models as m
import const
from . import fixture as f


__all__ = [
    'f',
    'h',
    'j',
    'm',
    'r',
    'const',
    'datetime',
    'mock',
    'random',
    'uuid',
    'BaseTestCase',
]


class _BaseTestCase(TestCase):

    token = None

    def create_app(self):
        current_app = app.create_app(__name__)
        current_app.config['TESTING'] = True
        return current_app

    def setUp(self):
        db.create_all()
        r.flushdb()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # BUG: alembic_version will not be dropped since it has no ORM model.
        db.engine.execute('drop table if exists alembic_version')
        r.flushdb()


class BaseTestCase(_BaseTestCase):

    def login_headers(self, account, app=None):
        account = account or f.Account()
        token = m.Token.add(account_id=account.id)
        self._token = token
        headers = {
            'Authorization': 'Bearer ' + token.token,
        }
        return headers

    def req(self, method, url, body=None, account=None, headers=None):
        func = getattr(self.client, method, None)
        self.assertTrue(callable(func))
        headers_ = self.login_headers(account)
        if headers:
            headers_.update(headers)
        resp = func(url, data=j.dumps(body), headers=headers_)
        return resp

    def get(self, url, account=None, headers=None):
        return self.req('get', url, None, account, headers)

    def post(self, url, body=None, account=None, headers=None):
        return self.req('post', url, body, account, headers)

    def put(self, url, body=None, account=None, headers=None):
        return self.req('put', url, body, account, headers)

    def patch(self, url, body=None, account=None, headers=None):
        return self.req('patch', url, body, account, headers)

    def delete(self, url, body=None, account=None, headers=None):
        return self.req('delete', url, body, account, headers)

    def assert_page(self, resp, length, total):
        self.assertEqual(resp.status_code, h.OK.value)
        self.assertTrue(isinstance(resp.json, list))

        length_ = len(resp.json)
        self.assertEqual(length_, length)

        total_ = int(resp.headers.get('X-Total') or -1)
        self.assertEqual(total_, total)

    def assert_field_error(self, errors, schema, field, error_type='validator_failed', message=None):
        origin = errors.get(field)
        self.assertIsNotNone(origin)
        target_error_messages = schema.__dict__['_declared_fields'][field].error_messages[error_type]
        target_validate = schema.__dict__['_declared_fields'][field].validate
        if target_error_messages and target_error_messages != 'Invalid value.':
            target = target_error_messages
            self.assertIn(target, origin)
        elif target_validate.__class__.__name__ == 'OneOf':
            target = target_validate.error
            self.assertIn(target, origin)

        elif isinstance(target_validate, list):
            t_error = [t.error for t in target_validate]
            self.assertIn(origin[0], t_error)

    def get_schema_total_fields(self, schema):
        return schema._declared_fields.keys()

    def get_schema_required_fields(self, schema):
        required_fields = []
        for field in self.get_schema_total_fields(schema):
            if schema.__dict__['_declared_fields'][field].required:
                required_fields.append(field)
        return required_fields

    def get_schema_validate_fields(self, schema):
        validate_fields = []
        for field in self.get_schema_total_fields(schema):
            if schema.__dict__['_declared_fields'][field].validate:
                validate_fields.append(field)
        return validate_fields

    def assert_schema_required_fields(self, method, url, body, schema, account=None, excludes=None):
        resp = self.req(method, url, body, account or f.Admin())
        self.assertEquals(resp.status_code, h.UNPROCESSABLE_ENTITY)
        errors = resp.json.get('errors') or {}
        required_fields = list(set(self.get_schema_required_fields(schema)) - set(excludes or []))
        actual_fields = [r for r in required_fields if r in errors.keys()]
        self.assertEquals(required_fields, actual_fields)

    def assert_schema_failed_fields(self, method, url, body, schema, account=None, excludes=None):
        resp = self.req(method, url, body, account or f.Admin())
        self.assertEquals(resp.status_code, h.UNPROCESSABLE_ENTITY)
        validate_fields = list(set(self.get_schema_validate_fields(schema)) - set(excludes or []))
        errors = resp.json.get('errors') or {}
        for field in validate_fields:
            self.assert_field_error(errors, schema, field)
