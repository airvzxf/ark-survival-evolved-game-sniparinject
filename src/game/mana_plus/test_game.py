#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Unit Test.
"""
from unittest.mock import MagicMock, patch, call

from scapy.layers.inet import IP
from scapy.packet import Raw

from game.mana_plus.game import Game


class TestGame:
    style_error = '\x1b[00;37;41m'
    style_end = '\x1b[0m'

    @patch('game.mana_plus.game.Game._start_node')
    def test___init__(self, mock_start_node: MagicMock):
        # Arrange
        expected_data = b'\x01\x02\x03'
        expected_packet = IP() / Raw(expected_data)

        # Act
        game = Game('Anything', expected_packet)

        # Assert
        assert game.raw_data == expected_data
        assert game.raw_data_copy == expected_data
        mock_start_node.assert_called_once()

    @patch('game.mana_plus.game.Game._start_host')
    def test___init___host(self, mock_start_host: MagicMock):
        # Arrange
        expected_host_ip = '129.185.210.19'
        expected_packet = IP(src=expected_host_ip) / Raw()

        # Act
        Game(expected_host_ip, expected_packet)

        # Assert
        mock_start_host.assert_called_once()

    @patch('game.mana_plus.game.Host')
    @patch('game.mana_plus.game.host')
    @patch('game.mana_plus.game.reload')
    def test__start_host(self, mock_reload: MagicMock, mock_host: MagicMock, mock_host_class: MagicMock):
        # Arrange
        expected_data = b'\x01\x02\x03'
        host_ip = '129.185.210.19'
        expected_packet = IP(src=host_ip) / Raw(expected_data)

        # Act
        game = Game(host_ip, expected_packet)

        # Assert
        mock_reload.assert_called_once_with(mock_host)
        mock_host_class.assert_called_once_with(game.raw_data)

    @patch('builtins.print')
    @patch('game.mana_plus.game.reload')
    def test__start_host_catch_exception(self, mock_reload: MagicMock, mock_print: MagicMock):
        # Arrange
        expected_error = 'KaBoom!'
        expected_data = b'\x01\x03\x05\x07'
        host_ip = '129.185.210.19'
        expected_packet = IP(src=host_ip) / Raw(expected_data)
        mock_reload.side_effect = Exception(expected_error)

        # Act
        Game(host_ip, expected_packet)

        # Assert
        mock_print.assert_has_calls([
            call(f'{self.style_error}Error Host: {expected_error}{self.style_end}'),
            call(f'{self.style_error}            {expected_data.hex()}{self.style_end}'),
        ])

    @patch('game.mana_plus.game.Node')
    @patch('game.mana_plus.game.node')
    @patch('game.mana_plus.game.reload')
    def test__start_node(self, mock_reload: MagicMock, mock_node: MagicMock, mock_node_class: MagicMock):
        # Arrange
        expected_data = b'\x01\x02\x03'
        expected_packet = IP() / Raw(expected_data)

        # Act
        game = Game('Hello friend', expected_packet)

        # Assert
        mock_reload.assert_called_once_with(mock_node)
        mock_node_class.assert_called_once_with(game.raw_data)

    @patch('builtins.print')
    @patch('game.mana_plus.game.reload')
    def test__start_node_catch_exception(self, mock_reload: MagicMock, mock_print: MagicMock):
        # Arrange
        expected_error = 'CheBoom!'
        expected_data = b'\x01\x03\x05\x07'
        expected_packet = IP() / Raw(expected_data)
        mock_reload.side_effect = Exception(expected_error)

        # Act
        Game('Whatever', expected_packet)

        # Assert
        mock_print.assert_has_calls([
            call(f'{self.style_error}Error Node: {expected_error}{self.style_end}'),
            call(f'{self.style_error}            {expected_data.hex()}{self.style_end}'),
        ])
