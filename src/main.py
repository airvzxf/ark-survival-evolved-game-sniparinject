#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
ARK Game: Read the network packets is an effort to use WireShark and scan the packet to know
your current position and get more information in the play game.
"""
from sniparinject.network_sniffer import NetworkSniffer

if __name__ == '__main__':
    SETTINGS_PATH = 'settings.yml'
    NetworkSniffer(SETTINGS_PATH).start()
