#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Unit Test.
"""
from unittest.mock import patch, MagicMock

from game.mana_plus.host import Host


class TestHost:
    style_title = '\x1b[00;93;44m'
    style_normal = '\x1b[00;30;44m'
    style_bold = '\x1b[00;37;44m'
    style_light = '\x1b[00;96;44m'
    style_end = '\x1b[0m'

    @patch('game.mana_plus.host.Host._start')
    @patch('game.mana_plus.host.Utility.__init__')
    def test___init__(self, mock_utility: MagicMock, mock_start: MagicMock):
        # Arrange
        expected_data = b'\x01\x03\x05'

        # Act
        host = Host(expected_data)

        # Assert
        assert host.raw_data == expected_data
        assert host.raw_data_copy == expected_data
        assert host.display_info is True
        assert len(host.actions) > 0
        assert len(host.npc_monster) > 0
        mock_utility.assert_called_once_with(
            'host', host.display_info, host.raw_data,
            host.raw_data_copy, host.actions
        )
        mock_start.assert_called_once()

    @patch('game.mana_plus.host.Host._start')
    def test__npc_monster_check(self, mock_start: MagicMock):
        # Arrange
        data = b'\x7a\x8c\xf1\x34\x5e'
        expected_message = f'{self.style_title}<-- NPC Monster Check{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 0x34f18c7a{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Unknown{self.style_end}'
        expected_message += f'{self.style_light} 5e{self.style_end}'
        mock_start.return_value = True

        # Act
        host = Host(data)
        message = host._npc_monster_check()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.host.Host._start')
    def test__player_move(self, mock_start: MagicMock):
        # Arrange
        data = b'\x23\x30\xe3\xf3\x16\xc4\x61\x70\x46\x00'
        expected_message = f'{self.style_title}<-- Player move to{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 0xf3e33023{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} XY{self.style_end}'
        expected_message += f'{self.style_light} 16c4617046{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Unknown{self.style_end}'
        expected_message += f'{self.style_light} 00{self.style_end}'
        mock_start.return_value = True

        # Act
        host = Host(data)
        message = host._player_move()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.host.Host._start')
    def test__npc_monster_move_to(self, mock_start: MagicMock):
        # Arrange
        data = b'\xbb\x8e\x8e\x06\xe8\x02\x00\x00\x00\x00\x00\x00\x59\x04\x00\x00\x00' \
               b'\x00\x00\x00\x79\xc6\xed\xf3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x20\x01\x00\x00\x20\x01\x00\x00\x00\x00\x00\x00\x01\x00\x16\xc3\x91' \
               b'\x70\x30\x00\x00\x00\x00\x00'
        expected_message = f'{self.style_title}<-- NPC Move{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 00x68e8ebb{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} e8 02{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} NPC{self.style_end}'
        expected_message += f'{self.style_light} Pollett{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0 0{self.style_end}'
        expected_message += f'{self.style_light} 0xf3edc679 0{self.style_end}'
        expected_message += f'{self.style_light} 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} HP{self.style_end}'
        expected_message += f'{self.style_light} 288{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} HP Max{self.style_end}'
        expected_message += f'{self.style_light} 288{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 1{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} XY{self.style_end}'
        expected_message += f'{self.style_light} 16c3917030{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0 00{self.style_end}'
        mock_start.return_value = True

        # Act
        host = Host(data)
        message = host._npc_monster_move_to()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.host.Host._start')
    def test__npc_monster_move_to_unknown_value(self, mock_start: MagicMock):
        # Arrange
        data = b'\xbb\x8e\x8e\x06\xe8\x02\x00\x00\x00\x00\x00\x00\xcd\xab\x00\x00\x00' \
               b'\x00\x00\x00\x79\xc6\xed\xf3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x20\x01\x00\x00\x20\x01\x00\x00\x00\x00\x00\x00\x01\x00\x16\xc3\x91' \
               b'\x70\x30\x00\x00\x00\x00\x00'
        expected_message = f'{self.style_title}<-- NPC Move{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 00x68e8ebb{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} e8 02{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} NPC{self.style_end}'
        expected_message += f'{self.style_light} 0xabcd{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0 0{self.style_end}'
        expected_message += f'{self.style_light} 0xf3edc679 0{self.style_end}'
        expected_message += f'{self.style_light} 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} HP{self.style_end}'
        expected_message += f'{self.style_light} 288{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} HP Max{self.style_end}'
        expected_message += f'{self.style_light} 288{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 1{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} XY{self.style_end}'
        expected_message += f'{self.style_light} 16c3917030{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0 00{self.style_end}'
        mock_start.return_value = True

        # Act
        host = Host(data)
        message = host._npc_monster_move_to()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.host.Host._start')
    def test__fight(self, mock_start: MagicMock):
        # Arrange
        data = b'\x65\xdb\x22\x00\xbf\x8e\x8e\x06\x08\xf4\xfb\xf3\xf9\x01\x00\x00' \
               b'\xe0\x01\x00\x00\x2f\x00\x01\x00\x00\x00\x00'
        expected_message = f'{self.style_title}<-- Fight{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Attacker{self.style_end}'
        expected_message += f'{self.style_light} 000x22db65{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Target{self.style_end}'
        expected_message += f'{self.style_light} 00x68e8ebf{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0xf3fbf408{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 505{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 480{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} Attack{self.style_end}'
        expected_message += f'{self.style_light}   47{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 1{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 00{self.style_end}'
        mock_start.return_value = True

        # Act
        host = Host(data)
        message = host._fight()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.host.Host._start')
    def test__npc_info(self, mock_start: MagicMock):
        # Arrange
        data = b'\xd0\x8e\x8e\x06\x64\x03\x00\x00\x00\x00\x00\x00\x47\x04\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x64\x00\x00\x00\x64\x00\x00\x00\x00\x00\x00\x00\x02\x00\x15' \
               b'\x02\xa0\x00\x00\x00\x00\x00'
        expected_message = f'{self.style_title}<-- NPC Info{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 00x68e8ed0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 64 03{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} NPC{self.style_end}'
        expected_message += f'{self.style_light} White Bell{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} HP{self.style_end}'
        expected_message += f'{self.style_light}  100{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} HP Max{self.style_end}'
        expected_message += f'{self.style_light}  100{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 2{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} XY{self.style_end}'
        expected_message += f'{self.style_light} 1502a0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0 00{self.style_end}'
        mock_start.return_value = True

        # Act
        host = Host(data)
        message = host._npc_info()

        # Assert
        assert message == expected_message

    @patch('game.mana_plus.host.Host._start')
    def test__npc_info_unknown_value(self, mock_start: MagicMock):
        # Arrange
        data = b'\xd0\x8e\x8e\x06\x64\x03\x00\x00\x00\x00\x00\x00\xcd\xab\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x64\x00\x00\x00\x64\x00\x00\x00\x00\x00\x00\x00\x02\x00\x15' \
               b'\x02\xa0\x00\x00\x00\x00\x00'
        expected_message = f'{self.style_title}<-- NPC Info{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} ID{self.style_end}'
        expected_message += f'{self.style_light} 00x68e8ed0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 64 03{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} NPC{self.style_end}'
        expected_message += f'{self.style_light} 0xabcd{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} HP{self.style_end}'
        expected_message += f'{self.style_light}  100{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} HP Max{self.style_end}'
        expected_message += f'{self.style_light}  100{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0 0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 2{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_bold} XY{self.style_end}'
        expected_message += f'{self.style_light} 1502a0{self.style_end}'
        expected_message += f'{self.style_normal} |{self.style_end}'
        expected_message += f'{self.style_light} 0 00{self.style_end}'
        mock_start.return_value = True

        # Act
        host = Host(data)
        message = host._npc_info()

        # Assert
        assert message == expected_message
