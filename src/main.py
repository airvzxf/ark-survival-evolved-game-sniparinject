#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
ARK Game: Read the network packages is an effort to use WireShark and scan the package to know
your current position and get more information in the play game.
"""
from core.network_sniffer import NetworkSniffer
from core.settings import Settings

if __name__ == '__main__':
    print()
    print('=== Settings ===')
    settings = Settings('settings.yml').get_dictionary()
    print(settings)

    print()
    print('=== Network Sniffer ===')
    interface = settings.get('Network').get('interface')
    host = settings.get('Server').get('host')
    port = settings.get('Server').get('port')
    NetworkSniffer(interface, host, port).start()
