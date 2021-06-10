#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Unit Test.
"""
from unittest.mock import patch, MagicMock

from scapy.layers.inet import TCP
from scapy.layers.l2 import Ether
from scapy.packet import Raw

from core.network_sniffer import NetworkSniffer


class TestNetworkSniffer:
    style_error = '\x1b[00;37;41m'
    style_end = '\x1b[0m'

    def test___init__(self):
        # Arrange
        expected_interface = 'Iceberg'
        expected_host = 'Server to me'
        expected_port = '1234567890'

        # Act
        network_sniffer = NetworkSniffer(expected_interface, expected_host, expected_port)

        # Assert
        assert network_sniffer.interface == expected_interface
        assert network_sniffer.host == expected_host
        assert network_sniffer.port == expected_port

    @patch('core.network_sniffer.sniff')
    def test_start(self, mock_sniff: MagicMock):
        # Arrange
        expected_interface = 'Touch me'
        expected_host = 'Hosting'
        expected_port = '9990666'

        # Act
        network_sniffer = NetworkSniffer(expected_interface, expected_host, expected_port)
        network_sniffer.start()

        # Assert
        mock_sniff.assert_called_once_with(
            iface=expected_interface,
            filter=f'host {expected_host} and tcp port {expected_port}',
            count=0,
            prn=network_sniffer._sniff_data
        )

    @patch('core.network_sniffer.reload')
    def test__sniff_data_request_without_data(self, mock_reload: MagicMock):
        # Arrange
        # Act
        network_sniffer = NetworkSniffer('', '', '')
        network_sniffer._sniff_data(TCP())

        # Assert
        mock_reload.assert_not_called()

    @patch('core.network_sniffer.reload')
    def test__sniff_data_request_without_tcp(self, mock_reload: MagicMock):
        # Arrange
        # Act
        network_sniffer = NetworkSniffer('', '', '')
        network_sniffer._sniff_data(Raw(b'\xff'))

        # Assert
        mock_reload.assert_not_called()

    @patch('core.network_sniffer.game')
    @patch('core.network_sniffer.reload')
    def test__sniff_data_reload_game(self, mock_reload: MagicMock, mock_game: MagicMock):
        # Arrange
        mock_game.return_value = True

        # Act
        network_sniffer = NetworkSniffer('', '', '')
        network_sniffer._sniff_data(TCP() / Raw(b'\xff'))

        # Assert
        mock_reload.assert_called_once_with(mock_game)

    @patch('core.network_sniffer.game')
    @patch('core.network_sniffer.reload')
    def test__sniff_data_class_game(self, mock_reload: MagicMock, mock_game: MagicMock):
        # Arrange
        expected_host = 'goliath.com'
        expected_packet: Ether = TCP() / Raw(b'\x00\x01\x02')
        mock_reload.return_value = True

        # Act
        network_sniffer = NetworkSniffer('', expected_host, '')
        network_sniffer._sniff_data(expected_packet)

        # Assert
        mock_game.Game.assert_called_once_with(expected_host, expected_packet)

    @patch('builtins.print')
    @patch('core.network_sniffer.reload')
    def test__sniff_data_mana_plus_catch_general_error(self, mock_reload: MagicMock, mock_print: MagicMock):
        # Arrange
        expected_error = 'Boom!'
        packet: Ether = TCP() / Raw(b'\x00\x01\x02')
        mock_reload.side_effect = Exception(expected_error)

        # Act
        network_sniffer = NetworkSniffer('', '', '')
        network_sniffer._sniff_data(packet)

        # Assert
        mock_print.assert_called_once_with(
            f'{self.style_error}Error Network Sniffer: {expected_error}{self.style_end}'
        )