#!usr/bin/env python
# -*- coding: utf-8 -*-

from .base import *


class TestResourcesAccountLogout(BaseTestCase):
    def test_logout(self):
        resp = self.post('/api/v1/logout', None)
        self.assertEqual(resp.status_code, h.OK.value)

    def test_logout_failed(self):
        resp = self.post('/api/v1/logout', None, headers={'Authorization': ''})
        self.assertEqual(resp.status_code, h.UNAUTHORIZED.value)
