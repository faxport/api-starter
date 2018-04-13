#!usr/bin/env python
# -*- coding: utf-8 -*-

from .base import *


class TestResourcesAccountSignup(BaseTestCase):
    def test_signup(self):
        account = f.Account.build()
        body = {
            'email': account.email,
            'password': 'password',
        }
        resp = self.post('/api/v1/signup', body)
        self.assertEqual(resp.status_code, h.CREATED.value)
        self.assertIsNotNone(resp.json.get('access_token'))

    def test_signup_failed_with_existed_fields(self):
        existed = f.Account()
        account = f.Account.build()

        # existed email
        body = {
            'email': existed.email,
            'password': 'password',
        }
        resp = self.post('/api/v1/signup', body)
        self.assertEqual(resp.status_code, h.UNPROCESSABLE_ENTITY.value)
