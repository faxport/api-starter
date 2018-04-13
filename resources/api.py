#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restful import Api

from .account import *


urls_account = [
    (LoginResource, '/login'),
    (LogoutResource, '/logout'),
    (ProfileResource, '/profile'),
    (SignupResource, '/signup'),
]


urls = urls_account

# create bp and api, add all resources.
bp = Blueprint('api', __name__)
api = Api(bp, prefix='/api/v1')

for i in urls:
    api.add_resource(*i)
