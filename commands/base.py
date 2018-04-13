#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = [
    'manager',
]

from flask_script import Manager

import app
import utils

manager = Manager(app.create_app)


@manager.command
def routes():
    """Show routes of all endpoints"""
    result = utils.flask.routes()
    header = '{:50s} {:50s} {}'.format('Endpoint', 'Methods', 'URL')
    print(header)
    for route in sorted(result, key=lambda i: i['url']):
        line = '{endpoint:50s} {methods:50s} {url}'.format(**route)
        print(line)
