#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = [
    'AccountRole',
]

from .base import Base


class AccountRole(Base):
    ADMIN = 1
    USER = 2


if __name__ == '__main__':
    # list all enum values
    print(AccountRole.values())

    # choice random enum value
    print(AccountRole.choice())

    # enum value to human name
    # eg: AccountRole.ADMIN.value => 'admin'
    print(AccountRole.to_name(AccountRole.ADMIN.value))
