#!/usr/bin/env python
# -*- coding: utf-8 -*-

import const
import decorators
import models as m
import serializers
import schemas
import services
from ..base import BaseResource


class SignupResource(BaseResource):
    @decorators.capture_exc
    @decorators.validate(schemas.AccountSignupPostSchema)
    @decorators.serialize(serializers.AccountWithTokenSerializer)
    def post(self):
        record = m.Account.add(**self.body)
        record.access_token = m.Token.add(account_id=record.id).token
        return record, 201, {}
