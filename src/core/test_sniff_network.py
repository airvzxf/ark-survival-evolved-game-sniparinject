#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Unit Test.
"""
from unittest.mock import patch, MagicMock

from scapy.layers.inet import TCP
from scapy.layers.l2 import Ether
from scapy.packet import Raw

from core.sniff_network import SniffNetwork


class TestSniffNetwork:
    def test___init__(self):
        # Arrange
        expected_interface = 'Iceberg'
        expected_host = 'Server to me'
        expected_port = '1234567890'

        # Act
        sniff_network = SniffNetwork(expected_interface, expected_host, expected_port)

        # Assert
        assert sniff_network.interface == expected_interface
        assert sniff_network.host == expected_host
        assert sniff_network.port == expected_port

    @patch('core.sniff_network.sniff')
    def test_start(self, mock_sniff: MagicMock):
        # Arrange
        expected_interface = 'Touch me'
        expected_host = 'Hosting'
        expected_port = '9990666'

        # Act
        sniff_network = SniffNetwork(expected_interface, expected_host, expected_port)
        sniff_network.start()

        # Assert
        mock_sniff.assert_called_once_with(
            iface=expected_interface,
            filter=f'host {expected_host} and tcp port {expected_port}',
            count=0,
            prn=sniff_network._sniff_data
        )

    @patch('core.sniff_network.reload')
    def test__sniff_data_request_without_data(self, mock_reload: MagicMock):
        # Arrange
        # Act
        sniff_network = SniffNetwork('', '', '')
        sniff_network._sniff_data(TCP())

        # Assert
        mock_reload.assert_not_called()

    @patch('core.sniff_network.reload')
    def test__sniff_data_request_without_tcp(self, mock_reload: MagicMock):
        # Arrange
        # Act
        sniff_network = SniffNetwork('', '', '')
        sniff_network._sniff_data(Raw(b'\xff'))

        # Assert
        mock_reload.assert_not_called()

    @patch('core.sniff_network.game')
    @patch('core.sniff_network.reload')
    def test__sniff_data_reload_game(self, mock_reload: MagicMock, mock_game: MagicMock):
        # Arrange
        mock_game.return_value = True

        # Act
        sniff_network = SniffNetwork('', '', '')
        sniff_network._sniff_data(TCP() / Raw(b'\xff'))

        # Assert
        mock_reload.assert_called_once_with(mock_game)

    @patch('core.sniff_network.game')
    @patch('core.sniff_network.reload')
    def test__sniff_data_class_game(self, mock_reload: MagicMock, mock_game: MagicMock):
        # Arrange
        expected_host = 'goliath.com'
        expected_packet: Ether = TCP() / Raw(b'\x00\x01\x02')
        mock_reload.return_value = True

        # Act
        sniff_network = SniffNetwork('', expected_host, '')
        sniff_network._sniff_data(expected_packet)

        # Assert
        mock_game.Game.assert_called_once_with(expected_host, expected_packet)

    @patch('builtins.print')
    @patch('core.sniff_network.reload')
    def test__sniff_data_mana_plus_catch_general_error(self, mock_reload: MagicMock, mock_print: MagicMock):
        # Arrange
        expected_error = 'Boom!'
        packet: Ether = TCP() / Raw(b'\x00\x01\x02')
        mock_reload.side_effect = Exception(expected_error)

        # Act
        sniff_network = SniffNetwork('', '', '')
        sniff_network._sniff_data(packet)

        # Assert
        mock_print.assert_called_once_with(f'Error: {expected_error}')
