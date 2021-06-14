#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Start the sniff of the network packets.
"""
from scapy.layers.inet import TCP
from scapy.layers.l2 import Ether
from scapy.packet import Raw
from scapy.sendrecv import sniff

from core.game import Game
from core.settings import Settings


# pylint: disable=too-few-public-methods
class NetworkSniffer:
    """
    Init the sniff of the network for spy the packets.
    """

    def __init__(self, settings_path: str) -> None:
        """
        Init the sniff of the network for spy the packets.

        :type settings_path: dict
        :param settings_path: The path of the YAML file with settings.

        :rtype: None
        :return: Nothing.
        """
        self.settings_path = settings_path
        print()
        print('=== Settings ===')
        settings = Settings(settings_path).get_dictionary()
        print(settings)

        self.interface = settings.get('Network').get('interface')
        self.host = settings.get('Server').get('host')
        self.port = settings.get('Server').get('port')
        print()
        print('=== Network Sniffer ===')
        print(f'Interface: {self.interface}')
        print(f'Host:      {self.host}')
        print(f'Port:      {self.port}')
        print()

    def start(self) -> None:
        """
        Start the sniffer.

        :rtype: None
        :return: Nothing.
        """
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
            Game(self.settings_path, self.host, packet).start()
