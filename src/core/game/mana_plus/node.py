#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Manage the node connection of Mana Plus.
"""
from struct import unpack

from core.game.text_style import TextStyle
from core.game.utility import Utility


class ManaPlusNode(Utility):
    """
    Manage the node connection.
    """

    def __init__(self, raw_data: bytes):
        """
        Initialize the class.

        :type raw_data: bytes
        :param raw_data: The raw data in bytes.

        :rtype: None
        :return: Nothing.
        """
        self.display_info = True
        self.raw_data = raw_data
        self.raw_data_copy = raw_data

        self.actions = {
            0x7d: self._scenario_change,
            0x85: self._player_move_to,
            0x89: self._player_action,
            0x90: self._npc_dialog_open,
            0x94: self._character_visible,
            0x9b: self._player_smash_with_object,
            0x9f: self._player_pickup_item,
            0xb8: self._npc_dialog_option_display,
            0xb9: self._npc_dialog_next,
            0xbf: self._connect_server_constant_1,
            0xc5: self._shop_store,
            0xc8: self._shop_buy_item,
            0xc9: self._shop_shell_item,
            0x118: self._npc_killed,
            0x146: self._npc_dialog_close,
            0x210: self._connect_server_constant_2,
        }

        self.player_actions = {
            0x2: 'Sit down',
            0x3: 'Stan up',
            0x7: 'Attack',
        }

        super().__init__(
            'node', self.display_info, self.raw_data,
            self.raw_data_copy, self.actions)
        self._start()

    def _player_move_to(self) -> str:
        """
        Player moves to specific position.

        :rtype: str
        :return: Message of this action.
        """
        position_1, position_2, position_3 = unpack('<ccc', self._get_data(3))
        position_1 = position_1.hex()
        position_2 = position_2.hex()
        position_3 = position_3.hex()

        message = self.text_format('--> Player move to', TextStyle.TITLE)
        message += self.text_format(' |')
        message += self.text_format(f' {position_1}{position_2}{position_3}', TextStyle.LIGHT)

        return message

    def _player_action(self) -> str:
        """
        Player Action.

        :rtype: str
        :return: Message of this action.
        """
        id_target, action_id = unpack('<IB', self._get_data(5))
        id_target = hex(id_target).zfill(10)
        action_description = (
            ' = ' + self.player_actions.get(action_id)
            if action_id in self.player_actions.keys()
            else ''
        )
        action_id = hex(action_id)

        message = self.text_format('--> Player action', TextStyle.TITLE)
        message += self.text_format(' |')
        message += self.text_format(' Target', TextStyle.BOLD)
        message += self.text_format(f' {id_target}', TextStyle.LIGHT)
        message += self.text_format(' |')
        message += self.text_format(' ID', TextStyle.BOLD)
        message += self.text_format(f' {action_id}{action_description}', TextStyle.LIGHT)

        self.display_info = True
        return message

    def _npc_killed(self) -> str:
        """
        The NPC (Non-Player Character) was killed.

        :rtype: str
        :return: Message of this action.
        """
        return self.text_format('--> NPC was killed', TextStyle.TITLE)

    def _player_pickup_item(self) -> str:
        """
        Player pick up an item.

        :rtype: str
        :return: Message of this action.
        """
        action_id, unknown_1, unknown_2, unknown_3 = unpack('<Bccc', self._get_data(4))
        action_id = hex(action_id)
        unknown_1 = unknown_1.hex()
        unknown_2 = unknown_2.hex()
        unknown_3 = unknown_3.hex()

        message = self.text_format('--> Player pick up an item', TextStyle.TITLE)
        message += self.text_format(' |')
        message += self.text_format(' ID', TextStyle.BOLD)
        message += self.text_format(f' {action_id}', TextStyle.LIGHT)
        message += self.text_format(' |')
        message += self.text_format(' Unknown', TextStyle.BOLD)
        message += self.text_format(f' {unknown_1} {unknown_2} {unknown_3}', TextStyle.LIGHT)

        # self.display_info = True
        return message

    def _character_visible(self) -> str:
        """
        The character is visible for me.

        :rtype: str
        :return: Message of this action.
        """
        id_target, = unpack('<I', self._get_data(4))
        id_target = hex(id_target).zfill(10)

        message = self.text_format('--> Character visible', TextStyle.TITLE)
        message += self.text_format(' |')
        message += self.text_format(' ID', TextStyle.BOLD)
        message += self.text_format(f' {id_target}', TextStyle.LIGHT)

        return message

    def _player_smash_with_object(self) -> str:
        """
        Player smash with an object.

        :rtype: str
        :return: Message of this action.
        """
        unknown_1, unknown_2, unknown_3 = unpack('<ccc', self._get_data(3))
        unknown_1 = unknown_1.hex()
        unknown_2 = unknown_2.hex()
        unknown_3 = unknown_3.hex()

        message = self.text_format('--> Player Smash with object', TextStyle.TITLE)
        message += self.text_format(' |')
        message += self.text_format(' Unknown', TextStyle.BOLD)
        message += self.text_format(f' {unknown_1} {unknown_2} {unknown_3}', TextStyle.LIGHT)

        # self.display_info = True
        return message

    def _npc_dialog_open(self) -> str:
        """
        Start to talk with an NPC, the dialog is open.

        :rtype: str
        :return: Message of this action.
        """
        id_dialog, sub_dialog = unpack('<Ic', self._get_data(5))
        id_dialog = hex(id_dialog).zfill(10)
        sub_dialog, = sub_dialog.hex()

        message = self.text_format('--> NPC Dialog open', TextStyle.TITLE)
        message += self.text_format(' |')
        message += self.text_format(' ID', TextStyle.BOLD)
        message += self.text_format(f' {id_dialog}', TextStyle.LIGHT)
        message += self.text_format(' |')
        message += self.text_format(' Sub-dialog', TextStyle.BOLD)
        message += self.text_format(f' {sub_dialog}', TextStyle.LIGHT)

        return message

    def _npc_dialog_next(self) -> str:
        """
        Talking with an NPC, display next dialog.

        :rtype: str
        :return: Message of this action.
        """
        id_dialog, = unpack('<I', self._get_data(4))
        id_dialog = hex(id_dialog).zfill(10)

        message = self.text_format('--> NPC Dialog next', TextStyle.TITLE)
        message += self.text_format(' |')
        message += self.text_format(' ID', TextStyle.BOLD)
        message += self.text_format(f' {id_dialog}', TextStyle.LIGHT)

        return message

    def _npc_dialog_option_display(self) -> str:
        """
        Talking with an NPC, display new dialog based on the selected option.

        :rtype: str
        :return: Message of this action.
        """
        id_dialog, sub_dialog = unpack('<Ic', self._get_data(5))
        id_dialog = hex(id_dialog).zfill(10)
        sub_dialog, = sub_dialog.hex()

        message = self.text_format('--> NPC Dialog conversation', TextStyle.TITLE)
        message += self.text_format(' |')
        message += self.text_format(' ID', TextStyle.BOLD)
        message += self.text_format(f' {id_dialog}', TextStyle.LIGHT)
        message += self.text_format(' |')
        message += self.text_format(' Sub-dialog', TextStyle.BOLD)
        message += self.text_format(f' {sub_dialog}', TextStyle.LIGHT)

        return message

    def _npc_dialog_close(self) -> str:
        """
        Talking with an NPC, the dialog is close.

        :rtype: str
        :return: Message of this action.
        """
        id_dialog, = unpack('<I', self._get_data(4))
        id_dialog = hex(id_dialog).zfill(10)

        message = self.text_format('--> NPC Dialog close', TextStyle.TITLE)
        message += self.text_format(' |')
        message += self.text_format(' ID', TextStyle.BOLD)
        message += self.text_format(f' {id_dialog}', TextStyle.LIGHT)

        return message

    def _shop_store(self) -> str:
        """
        Open the shop storage.

        :rtype: str
        :return: Message of this action.
        """
        id_dialog, = unpack('<I', self._get_data(4))
        id_dialog = hex(id_dialog).zfill(10)

        message = self.text_format('--> Shop store', TextStyle.TITLE)
        message += self.text_format(' |')
        message += self.text_format(' ID', TextStyle.BOLD)
        message += self.text_format(f' {id_dialog}', TextStyle.LIGHT)

        return message

    def _shop_buy_item(self) -> str:
        """
        Buy an item.

        :rtype: str
        :return: Message of this action.
        """
        unknown_1, unknown_2, quantity, id_item, = unpack('<ccHH', self._get_data(6))
        id_item = hex(id_item).zfill(6)
        unknown_1 = unknown_1.hex()
        unknown_2 = unknown_2.hex()

        message = self.text_format('--> Shop buy item', TextStyle.TITLE)
        message += self.text_format(' |')
        message += self.text_format(' Unknown', TextStyle.BOLD)
        message += self.text_format(f' {unknown_1} {unknown_2}', TextStyle.LIGHT)
        message += self.text_format(' |')
        message += self.text_format(' Quantity', TextStyle.BOLD)
        message += self.text_format(f' {quantity}', TextStyle.LIGHT)
        message += self.text_format(' |')
        message += self.text_format(' ID', TextStyle.BOLD)
        message += self.text_format(f' {id_item}', TextStyle.LIGHT)

        # self.display_info = True
        return message

    def _shop_shell_item(self) -> str:
        """
        Shell an item.

        :rtype: str
        :return: Message of this action.
        """
        unknown_1, unknown_2, id_item, quantity, = unpack('<ccHH', self._get_data(6))
        id_item = hex(id_item).zfill(6)
        unknown_1 = unknown_1.hex()
        unknown_2 = unknown_2.hex()

        message = self.text_format('--> Shop shell item', TextStyle.TITLE)
        message += self.text_format(' |')
        message += self.text_format(' Unknown', TextStyle.BOLD)
        message += self.text_format(f' {unknown_1} {unknown_2}', TextStyle.LIGHT)
        message += self.text_format(' |')
        message += self.text_format(' ID', TextStyle.BOLD)
        message += self.text_format(f' {id_item}', TextStyle.LIGHT)
        message += self.text_format(' |')
        message += self.text_format(' Quantity', TextStyle.BOLD)
        message += self.text_format(f' {quantity}', TextStyle.LIGHT)

        # self.display_info = True
        return message

    def _scenario_change(self) -> str:
        """
        The scenario was changed.

        :rtype: str
        :return: Message of this action.
        """
        return self.text_format('--> Scenario change', TextStyle.TITLE)

    def _connect_server_constant_1(self) -> str:
        """
        The node is communicate with the server constantly.

        :rtype: str
        :return: Message of this action.
        """
        unknown_1, = unpack('<c', self._get_data(1))
        unknown_1 = unknown_1.hex()

        message = self.text_format('--> Communicate with the server [0xbf]', TextStyle.TITLE)
        message += self.text_format(' |')
        message += self.text_format(' Unknown', TextStyle.BOLD)
        message += self.text_format(f' {unknown_1}', TextStyle.LIGHT)

        return message

    def _connect_server_constant_2(self) -> str:
        """
        The node is communicate with the server constantly but not frequently.

        :rtype: str
        :return: Message of this action.
        """
        return self.text_format('--> Communicate with the server [0x210]', TextStyle.TITLE)
