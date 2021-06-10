#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Start the sniff of the network packets.
"""
from importlib import reload

from scapy.layers.inet import TCP
from scapy.layers.l2 import Ether
from scapy.packet import Raw
from scapy.sendrecv import sniff

from core.utility import Utility
from game.mana_plus import game


# pylint: disable=too-few-public-methods
class NetworkSniffer:
    """
    Init the sniff of the network for spy the packets.
    """

    def __init__(self, interface: str, host: str, port: str) -> None:
        """
        Initialize the class.

        :type interface: str
        :param interface: Network interface in ethernet cable could be en0, enp4s0,
        on WiFi could be wlp2s0.

        :type host: str
        :param host: IP of the host means source or destination.

        :type port: str
        :param port: Connected port of the host.

        :rtype: None
        :return: Nothing.
        """
        self.interface = interface
        self.host = host
        self.port = port

    def start(self) -> None:
        """
        Start the sniffer.

        :rtype: None
        :return: Nothing.
        """
        print(f'Interface: {self.interface}')
        print(f'Host:      {self.host}')
        print(f'Port:      {self.port}')
        print()

        sniff(
            iface=self.interface,
            filter=f'host {self.host} and tcp port {self.port}',
            count=0,
            prn=self._sniff_data
        )

    def _sniff_data(self, packet: Ether) -> None:
        """
        Process data provided by the Sniffer.

        :type packet: Ether
        :param packet: The sniffed packet.

        :rtype: None
        :return: Nothing.
        """
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            # pylint: disable=broad-except
            try:
                reload(game)
                game.Game(self.host, packet)
            except Exception as error:
                message = Utility.text_error_format(f'Error Network Sniffer: {error}')
                print(message)