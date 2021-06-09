#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Unit Test.
"""
from unittest.mock import patch, MagicMock

from scapy.layers.inet import TCP
from scapy.layers.l2 import Ether
from scapy.packet import Raw

from core.sniffer_network import SnifferNetwork


class TestSnifferNetwork:
    def test___init__(self):
        # Arrange
        expected_interface = 'Iceberg'
        expected_host = 'Server to me'
        expected_port = '1234567890'

        # Act
        sniffer_network = SnifferNetwork(expected_interface, expected_host, expected_port)

        # Assert
        assert sniffer_network.interface == expected_interface
        assert sniffer_network.host == expected_host
        assert sniffer_network.port == expected_port

    @patch('core.sniffer_network.sniff')
    def test_start(self, mock_sniff: MagicMock):
        # Arrange
        expected_interface = 'Touch me'
        expected_host = 'Hosting'
        expected_port = '9990666'

        # Act
        sniffer_network = SnifferNetwork(expected_interface, expected_host, expected_port)
        sniffer_network.start()

        # Assert
        mock_sniff.assert_called_once_with(
            iface=expected_interface,
            filter=f'host {expected_host} and tcp port {expected_port}',
            count=0,
            prn=sniffer_network._sniff_data
        )

    @patch('core.sniffer_network.reload')
    def test__sniff_data_request_without_data(self, mock_reload: MagicMock):
        # Arrange
        # Act
        sniffer_network = SnifferNetwork('', '', '')
        sniffer_network._sniff_data(TCP())

        # Assert
        mock_reload.assert_not_called()

    @patch('core.sniffer_network.reload')
    def test__sniff_data_request_without_tcp(self, mock_reload: MagicMock):
        # Arrange
        # Act
        sniffer_network = SnifferNetwork('', '', '')
        sniffer_network._sniff_data(Raw(b'\xff'))

        # Assert
        mock_reload.assert_not_called()

    @patch('core.sniffer_network.mana_plus')
    @patch('core.sniffer_network.reload')
    def test__sniff_data_reload_mana_plus(self, mock_reload: MagicMock, mock_mana_plus: MagicMock):
        # Arrange
        mock_reload.reset_mock()
        mock_mana_plus.reset_mock()
        mock_mana_plus.return_value = True

        # Act
        sniffer_network = SnifferNetwork('', '', '')
        sniffer_network._sniff_data(TCP() / Raw(b'\xff'))

        # Assert
        mock_reload.assert_called_once_with(mock_mana_plus)

    @patch('core.sniffer_network.mana_plus')
    @patch('core.sniffer_network.reload')
    def test__sniff_data_class_mana_plus(self, mock_reload: MagicMock, mock_mana_plus: MagicMock):
        # Arrange
        expected_host = 'goliath.com'
        expected_packet: Ether = TCP() / Raw(b'\x00\x01\x02')
        mock_mana_plus.reset_mock()
        mock_reload.reset_mock()
        mock_reload.return_value = True

        # Act
        sniffer_network = SnifferNetwork('', expected_host, '')
        sniffer_network._sniff_data(expected_packet)

        # Assert
        mock_mana_plus.ManaPlus.assert_called_once_with(expected_host, expected_packet)

    @patch('builtins.print')
    @patch('core.sniffer_network.reload')
    def test__sniff_data_mana_plus_catch_general_error(self, mock_reload: MagicMock, mock_print: MagicMock):
        # Arrange
        expected_error = 'Boom!'
        packet: Ether = TCP() / Raw(b'\x00\x01\x02')
        mock_print.reset_mock()
        mock_reload.reset_mock()
        mock_reload.side_effect = Exception(expected_error)

        # Act
        sniffer_network = SnifferNetwork('', '', '')
        sniffer_network._sniff_data(packet)

        # Assert
        mock_print.assert_called_once_with(f'Error: {expected_error}')
