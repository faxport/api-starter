#!usr/bin/env python
# -*- coding: utf-8 -*-

from .base import *

import decorators
import resources
import schemas


class TestSchemasAccount(BaseTestCase):

    def test_login_schema(self):
        schema = schemas.AccountLoginPostSchema
        url = '/api/v1/login'
        self.assert_schema_required_fields('post', url, {}, schema, f.Account())

        body = {
            'email': 'invalid',
            'password': 'invalid',
        }
        self.assert_schema_failed_fields('post', url, {}, schema, f.Account())

    def test_signup_schema(self):
        schema = schemas.AccountSignupPostSchema
        url = '/api/v1/signup'
        self.assert_schema_required_fields('post', url, {}, schema, f.Account())

        body = {
            'email': 'invalid',
            'password': 'invalid',
        }
        self.assert_schema_failed_fields('post', url, {}, schema, f.Account())
