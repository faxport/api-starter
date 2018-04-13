#!/usr/bin/env python
# -*- coding: utf-8 -*-

import env

from flask_migrate import MigrateCommand

from commands import manager

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
