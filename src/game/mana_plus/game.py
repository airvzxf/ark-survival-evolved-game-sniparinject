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

from core.utility import Utility
from game.mana_plus import node, host
from game.mana_plus.host import Host
from game.mana_plus.node import Node


class Game:
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
            self._start_host()
        else:
            self._start_node()

    def _start_host(self) -> None:
        """
        Start to process the host packets.

        :rtype: None
        :return: Nothing.
        """
        try:
            reload(host)
            Host(self.raw_data)
        except Exception as error:
            message_error = Utility.text_error_format(f'Error Host: {error}')
            message_data = Utility.text_error_format(f'            {self.raw_data.hex()}')
            print(message_error)
            print(message_data)

    def _start_node(self) -> None:
        """
        Start to process the node packets.

        :rtype: None
        :return: Nothing.
        """
        try:
            reload(node)
            Node(self.raw_data)
        except Exception as error:
            message_error = Utility.text_error_format(f'Error Node: {error}')
            message_data = Utility.text_error_format(f'            {self.raw_data.hex()}')
            print(message_error)
            print(message_data)
