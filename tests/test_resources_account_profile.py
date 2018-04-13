#!usr/bin/env python
# -*- coding: utf-8 -*-

from .base import *


class TestResourcesAccountProfile(BaseTestCase):
    def test_get_profile(self):
        account = f.Account()
        resp = self.get('/api/v1/profile', account)
        self.assertEqual(resp.status_code, h.OK.value)
        self.assertEqual(resp.json['id'], account.id)

    def test_get_profile_failed(self):
        account = f.Account()
        resp = self.get('/api/v1/profile', account, headers={'Authorization': ''})
        self.assertEqual(resp.status_code, h.UNAUTHORIZED.value)
