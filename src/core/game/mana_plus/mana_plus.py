#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Sniff the Mana Plus game.
https://archlinux.org/packages/community/x86_64/manaplus/
"""
from importlib import reload

from scapy.compat import raw
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether
from scapy.packet import Raw

from core.game.mana_plus import host
from core.game.mana_plus import node
from core.game.mana_plus.host import ManaPlusHost
from core.game.mana_plus.node import ManaPlusNode


class ManaPlus:
    """
    Sniff the Mana Plus game.
    """

    def __init__(self, host_ip: str, packet: Ether):
        """
        Initialize the class.

        :type host_ip: str
        :param host_ip: IP of the host means source or destination.

        :type packet: Ether
        :param packet: Ethernet packet.

        :rtype: None
        :return: Nothing.
        """
        ip_layer = packet.getlayer(IP)
        raw_layer = packet.getlayer(Raw)
        self.raw_data = raw(raw_layer)
        self.raw_data_copy = raw(raw_layer)

        if host_ip == ip_layer.src:
            try:
                reload(host)
                ManaPlusHost(self.raw_data)
            except Exception as error:
                print(f'Error: {error}')
        else:
            try:
                reload(node)
                ManaPlusNode(self.raw_data)
            except Exception as error:
                print(f'Error: {error}')
