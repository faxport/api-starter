#!usr/bin/env python
# -*- coding: utf-8 -*-

from .base import *


class TestModelsAccount(BaseTestCase):
    def test_create(self):
        password = 'secretpass'
        account = f.Account()
        self.assertIsNotNone(account)
        self.assertIsNotNone(account.id)
        result = account.check_password(password)
        self.assertEqual(result, True)

    def test_set_password(self):
        password = 'password'
        account = f.Account()
        result = account.check_password(password)
        self.assertEqual(result, False)

        account.set_password(password)
        result = account.check_password(password)
        account.reload()
        self.assertEqual(result, True)
