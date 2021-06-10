#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Unit Test.
"""
from unittest.mock import patch, MagicMock

from game.mana_plus.node import Node


class TestNode:
    style_title = '\x1b[00;93;100m'
    style_normal = '\x1b[00;30;100m'
    style_bold = '\x1b[00;37;100m'
    style_light = '\x1b[00;96;100m'
    style_end = '\x1b[0m'

    @patch('game.mana_plus.node.Node._start')
    @patch('game.mana_plus.node.Utility.__init__')
    def test___init__(self, mock_utility: MagicMock, mock_start: MagicMock):
        # Arrange
        expected_data = b'\x01\x03\x05'

        # Act
        node = Node(expected_data)

        # Assert
        assert node.raw_data == expected_data
        assert node.raw_data_copy == expected_data
        assert node.display_info is True
        assert len(node.actions) > 0
        assert len(node.player_actions) > 0
        assert len(node.shop_options) > 0
        mock_utility.assert_called_once_with(
            'node', node.display_info, node.raw_data,
            node.raw_data_copy, node.actions
        )
        mock_start.assert_called_once()

    @patch('game.mana_plus.node.Node._start')
    def test__player_move_to(self, mock_start: MagicMock):
        # Arrange
        data = b'\x17\x03\x90'
        expected_message = f'{self.style_title}--> Player move to{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 170390{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._player_move_to()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__player_action(self, mock_start: MagicMock):
        # Arrange
        data = b'\xb6\x8e\x8e\x06\x07'
        expected_message = f'{self.style_title}--> Player action{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Target{self.style_end}'
        expected_message += f'{self.style_light} 00x68e8eb6{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} Attack{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._player_action()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__player_action_unknown_value(self, mock_start: MagicMock):
        # Arrange
        data = b'\xb6\x8e\x8e\x06\xe6'
        expected_message = f'{self.style_title}--> Player action{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Target{self.style_end}'
        expected_message += f'{self.style_light} 00x68e8eb6{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 0xe6{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._player_action()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__npc_killed(self, mock_start: MagicMock):
        # Arrange
        data = b''
        expected_message = f'{self.style_title}--> NPC was killed{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._npc_killed()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__player_pickup_item(self, mock_start: MagicMock):
        # Arrange
        data = b'\x02\x00\x00\x00'
        expected_message = f'{self.style_title}--> Player pick up an item{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 0x2{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Unknown{self.style_end}'
        expected_message += f'{self.style_light} 00 00 00{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._player_pickup_item()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__character_visible(self, mock_start: MagicMock):
        # Arrange
        data = b'\xd7\x8e\x8e\x06'
        expected_message = f'{self.style_title}--> Character visible{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 00x68e8ed7{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._character_visible()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__player_smash_with_object(self, mock_start: MagicMock):
        # Arrange
        data = b'\x00\x00\x02'
        expected_message = f'{self.style_title}--> Player Smash with object{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Unknown{self.style_end}'
        expected_message += f'{self.style_light} 00 00 02{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._player_smash_with_object()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__npc_dialog_open(self, mock_start: MagicMock):
        # Arrange
        data = b'\xd7\x8e\x8e\x06\x00'
        expected_message = f'{self.style_title}--> NPC Dialog open{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 00x68e8ed7{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Sub-dialog{self.style_end}'
        expected_message += f'{self.style_light} 00{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._npc_dialog_open()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__npc_dialog_next(self, mock_start: MagicMock):
        # Arrange
        data = b'\xd7\x8e\x8e\x06'
        expected_message = f'{self.style_title}--> NPC Dialog next{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 00x68e8ed7{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._npc_dialog_next()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__npc_dialog_option_display(self, mock_start: MagicMock):
        # Arrange
        data = b'\xd7\x8e\x8e\x06\x01'
        expected_message = f'{self.style_title}--> NPC Dialog conversation{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 00x68e8ed7{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Sub-dialog{self.style_end}'
        expected_message += f'{self.style_light} 01{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._npc_dialog_option_display()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__npc_dialog_close(self, mock_start: MagicMock):
        # Arrange
        data = b'\xd7\x8e\x8e\x06'
        expected_message = f'{self.style_title}--> NPC Dialog close{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 00x68e8ed7{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._npc_dialog_close()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__shop_store(self, mock_start: MagicMock):
        # Arrange
        data = b'\x46\x8a\x8e\x06\x01'
        expected_message = f'{self.style_title}--> Shop store{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Target{self.style_end}'
        expected_message += f'{self.style_light} 00x68e8a46{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} Sell{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._shop_store()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__shop_store_unknown_value(self, mock_start: MagicMock):
        # Arrange
        data = b'\x46\x8a\x8e\x06\x05'
        expected_message = f'{self.style_title}--> Shop store{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Target{self.style_end}'
        expected_message += f'{self.style_light} 00x68e8a46{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 0x5{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._shop_store()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__shop_buy_item(self, mock_start: MagicMock):
        # Arrange
        data = b'\x08\x00\x01\x00\x11\x02'
        expected_message = f'{self.style_title}--> Shop buy item{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Unknown{self.style_end}'
        expected_message += f'{self.style_light} 08 00{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Quantity{self.style_end}'
        expected_message += f'{self.style_light} 1{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 00x211{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._shop_buy_item()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__shop_shell_item(self, mock_start: MagicMock):
        # Arrange
        data = b'\x08\x00\x30\x00\x05\x00'
        expected_message = f'{self.style_title}--> Shop shell item{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Unknown{self.style_end}'
        expected_message += f'{self.style_light} 08 00{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 000x30{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Quantity{self.style_end}'
        expected_message += f'{self.style_light} 5{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._shop_shell_item()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__scenario_change(self, mock_start: MagicMock):
        # Arrange
        data = b''
        expected_message = f'{self.style_title}--> Scenario change{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._scenario_change()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__connect_server_constant_1(self, mock_start: MagicMock):
        # Arrange
        data = b'\xd2'
        expected_message = f'{self.style_title}--> Communicate with the server [0xbf]{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Unknown{self.style_end}'
        expected_message += f'{self.style_light} d2{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._connect_server_constant_1()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.node.Node._start')
    def test__connect_server_constant_2(self, mock_start: MagicMock):
        # Arrange
        data = b''
        expected_message = f'{self.style_title}--> Communicate with the server [0x210]{self.style_end}'
        mock_start.return_value = True

        # Act
        node = Node(data)
        message = node._connect_server_constant_2()

        # Assert
        assert message == expected_message
