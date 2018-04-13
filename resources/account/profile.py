#!/usr/bin/env python
# -*- coding: utf-8 -*-

import const
import decorators
import models as m
import serializers
import schemas
from ..base import BaseResource


class ProfileResource(BaseResource):
    @decorators.capture_exc
    @decorators.authorize()
    @decorators.serialize(serializers.AccountSerializer)
    def get(self):
        return self.current_account, 200, {}
