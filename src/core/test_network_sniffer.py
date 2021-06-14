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

    @patch('core.network_sniffer.Settings.get_dictionary')
    def test___init__(self, mock_settings: MagicMock):
        # Arrange
        expected_settings_path = 'my-non-settings.yml'
        expected_interface = 'Iceberg'
        expected_host = 'Server to me'
        expected_port = '1234567890'
        mock_settings.return_value = {
            'Network': {'interface': expected_interface},
            'Server': {'host': expected_host, 'port': expected_port},
        }

        # Act
        network_sniffer = NetworkSniffer(expected_settings_path)

        # Assert
        assert network_sniffer.settings_path == expected_settings_path
        assert network_sniffer.interface == expected_interface
        assert network_sniffer.host == expected_host
        assert network_sniffer.port == expected_port

    @patch('core.network_sniffer.Settings.get_dictionary')
    @patch('core.network_sniffer.sniff')
    def test_start(self, mock_sniff: MagicMock, mock_settings: MagicMock):
        # Arrange
        expected_interface = 'Touch me'
        expected_host = 'Hosting'
        expected_port = '9990666'
        mock_settings.return_value = {
            'Network': {'interface': expected_interface},
            'Server': {'host': expected_host, 'port': expected_port},
        }

        # Act
        network_sniffer = NetworkSniffer('any-settings.yml')
        network_sniffer.start()

        # Assert
        mock_sniff.assert_called_once_with(
            iface=expected_interface,
            filter=f'host {expected_host} and tcp port {expected_port}',
            count=0,
            prn=network_sniffer._sniff_data
        )

    @patch('core.network_sniffer.Settings.get_dictionary')
    @patch('core.network_sniffer.Game')
    def test__sniff_data_request_without_data(self, mock_game: MagicMock, mock_settings: MagicMock):
        # Arrange
        mock_settings.return_value = {
            'Network': {'interface': ''},
            'Server': {'host': '', 'port': 0},
        }

        # Act
        network_sniffer = NetworkSniffer('')
        network_sniffer._sniff_data(TCP())

        # Assert
        mock_game.assert_not_called()

    @patch('core.network_sniffer.Settings.get_dictionary')
    @patch('core.network_sniffer.Game')
    def test__sniff_data_request_without_tcp(self, mock_game: MagicMock, mock_settings: MagicMock):
        # Arrange
        mock_settings.return_value = {
            'Network': {'interface': ''},
            'Server': {'host': '', 'port': 0},
        }

        # Act
        network_sniffer = NetworkSniffer('')
        network_sniffer._sniff_data(Raw(b'\xff'))

        # Assert
        mock_game.assert_not_called()

    @patch('core.network_sniffer.Settings.get_dictionary')
    @patch('core.network_sniffer.Game')
    def test__sniff_data_class_game(self, mock_game: MagicMock, mock_settings: MagicMock):
        # Arrange
        expected_settings_path = 'hello-from-the-other-side.yml'
        expected_host = 'goliath.com'
        expected_packet: Ether = TCP() / Raw(b'\x00\x01\x02')
        mock_settings.return_value = {
            'Network': {'interface': ''},
            'Server': {'host': expected_host, 'port': 0},
        }

        # Act
        network_sniffer = NetworkSniffer(expected_settings_path)
        network_sniffer._sniff_data(expected_packet)

        # Assert
        mock_game.assert_called_once_with(
            expected_settings_path, expected_host, expected_packet)
