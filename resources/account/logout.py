#!/usr/bin/env python
# -*- coding: utf-8 -*-

import const
import decorators
import models as m
import schemas
from ..base import BaseResource


class LogoutResource(BaseResource):
    @decorators.capture_exc
    @decorators.authorize()
    def post(self):
        self.decoded_token.delete()
        return None, 200, {}
