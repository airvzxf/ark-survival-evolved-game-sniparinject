#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Start to sniff of the network.
"""
from scapy.compat import raw
from scapy.layers.inet import TCP, IP
from scapy.layers.l2 import Ether
from scapy.packet import Raw
from scapy.sendrecv import sniff


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

    @staticmethod
    def _sniff_data(packet: Ether) -> None:
        """
        Process data provided by the Sniffer.

        :type packet: Ether
        :param packet: The sniffed packet.

        :rtype: None
        :return: Nothing.
        """
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            ip_layer = packet.getlayer(IP)
            tcp_layer = packet.getlayer(TCP)
            raw_layer = packet.getlayer(Raw)

            print()
            print(f'--->'
                  f' | Src {ip_layer.src}:{ip_layer.sport}'
                  f' | Dst {ip_layer.dst}:{ip_layer.dport}'
                  f' | IP length: {len(ip_layer)}'
                  f' | TCP length: {len(tcp_layer)}'
                  f' | RAW length: {len(raw_layer)}'
                  )
            print(f'RAW: {raw(raw_layer).hex()}')
