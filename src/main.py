#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
ARK: Survival Evolved - Game: Intercept and read the network
packets to find information about the game.
"""
from sniparinject.network_sniffer import NetworkSniffer

if __name__ == '__main__':
    SETTINGS_PATH = 'settings.yml'
    NetworkSniffer(SETTINGS_PATH).start()
