#!/usr/bin/env python
# -*- coding: utf-8 -*-

import const
import decorators
import models as m
import serializers
import schemas
from ..base import BaseResource


class LoginResource(BaseResource):
    @decorators.capture_exc
    @decorators.validate(schemas.AccountLoginPostSchema)
    @decorators.serialize(serializers.AccountWithTokenSerializer)
    def post(self):
        msg_invalid = 'Invalid email or password'
        msg_not_found = 'Email has not been registered'
        record = m.Account.find_one_by(email=self.body['email'])
        if not record:
            self.raise_exc(code=422, message=msg_not_found)
        elif not record.check_password(self.body.get('password')):
            self.raise_exc(code=422, message=msg_invalid)
        record.access_token = m.Token.add(account_id=record.id).token
        return record, 200, {}
