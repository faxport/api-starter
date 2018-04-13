#!usr/bin/env python
# -*- coding: utf-8 -*-

from .base import *


class TestResourcesAccountLogin(BaseTestCase):
    def test_login(self):
        account = f.Account()
        body = {
            'email': account.email,
            'password': 'secretpass'
        }
        resp = self.post('/api/v1/login', body)
        self.assertEqual(resp.status_code, h.OK.value)
        self.assertIsNotNone(resp.json.get('access_token'))

    def test_login_with_email_case_insensitive(self):
        account = f.Account()
        body = {
            'email': account.email.upper(),
            'password': 'secretpass'
        }
        resp = self.post('/api/v1/login', body)
        self.assertEqual(resp.status_code, h.OK.value)
        self.assertIsNotNone(resp.json.get('access_token'))

    def test_login_failed(self):
        account = f.Account()
        body = {
            'email': account.email,
            'password': 'secretpass' + 'invalid'
        }
        resp = self.post('/api/v1/login', body)
        self.assertEqual(resp.status_code, h.UNPROCESSABLE_ENTITY.value)
