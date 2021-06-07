#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Start to sniff of the network.
"""
from importlib import reload

from scapy.layers.inet import TCP
from scapy.layers.l2 import Ether
from scapy.packet import Raw
from scapy.sendrecv import sniff

from core.game import mana_plus


class SnifferNetwork:
    """
    Init sniff of the network for spy the packages.
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

        sniff(
            iface=self.interface,
            filter=f'host {self.host} and tcp port {self.port}',
            count=0,
            prn=self._sniff_data)

    def _sniff_data(self, packet: Ether) -> None:
        """
        Process data provided by the Sniffer.

        :type packet: Ether
        :param packet: The sniffed packet.

        :rtype: None
        :return: Nothing.
        """
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            try:
                reload(mana_plus)
                mana_plus.ManaPlus(self.host, packet)
            except Exception as error:
                print(error)
