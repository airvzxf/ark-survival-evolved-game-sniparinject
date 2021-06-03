#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
ARK Game: Read the network packages is an effort to use WireShark and scan the package to know
your current position and get more information in the play game.
"""
from core.settings import Settings

if __name__ == '__main__':
    settings = Settings('settings.yml').get_dictionary()
    print()
    print('=== Settings ===')
    print(settings)
