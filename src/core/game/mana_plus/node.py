#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Manage the node connection of Mana Plus.
"""
from struct import unpack

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
        self.display_info = False
        self.raw_data = raw_data
        self.raw_data_copy = raw_data

        self.actions = {
            0x7d: self._scenario_change,
            0x85: self._player_move_to,
            0x89: self._player_action,
            0x90: self._npc_dialog_open,
            0x94: self._character_visible,
            0x9b: self._unknown_1_npc_monster_or_dropped_items,
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

        super().__init__('node', self.display_info, self.raw_data,
                         self.raw_data_copy, self.actions)
        self._start()

    def _player_move_to(self) -> str:
        """
        Player moves to specific position.

        :rtype: str
        :return: Message of this action.
        """
        position_1, position_2, position_3 = unpack('<ccc', self._get_data(3))

        return '--> Player move to' \
               f' | {position_1.hex()}{position_2.hex()}{position_3.hex()}'

    def _player_action(self) -> str:
        """
        Player Action.

        :rtype: str
        :return: Message of this action.
        """
        id_target = hex(unpack('<I', self._get_data(4))[0]).zfill(10)
        action_id, = unpack('<B', self._get_data(1))
        action_description = (
            ' = ' + self.player_actions.get(action_id)
            if action_id in self.player_actions.keys()
            else ''
        )

        self.display_info = True
        return '--> Player action' \
               f' | Target {id_target}' \
               f' | ID {hex(action_id)}{action_description}'

    @staticmethod
    def _npc_killed() -> str:
        """
        The NPC (Non-Player Character) was killed.

        :rtype: str
        :return: Message of this action.
        """
        return '--> NPC was killed'

    def _player_pickup_item(self) -> str:
        """
        Player pick up an item.

        :rtype: str
        :return: Message of this action.
        """
        action_id, = unpack('<B', self._get_data(1))
        unknown_1, unknown_2, unknown_3 = unpack('<ccc', self._get_data(3))

        # self.display_info = True
        return '--> Player pick up an item' \
               f' | ID {hex(action_id)}' \
               f' | Unknown {unknown_1.hex()} {unknown_2.hex()} {unknown_3.hex()}'

    def _character_visible(self) -> str:
        """
        The character is visible for me.

        :rtype: str
        :return: Message of this action.
        """
        id_target = hex(unpack('<I', self._get_data(4))[0]).zfill(10)

        return '--> Character visible' \
               f' | ID {id_target}'

    def _unknown_1_npc_monster_or_dropped_items(self) -> str:
        """
        Something is sending to the server related to the NPC Monsters or dropped items.

        :rtype: str
        :return: Message of this action.
        """
        unknown_1, unknown_2, unknown_3 = unpack('<ccc', self._get_data(3))

        # self.display_info = True
        return '--> Unknown 1 --> Related NPC Monsters or dropped Items' \
               f' | Unknown {unknown_1.hex()} {unknown_2.hex()} {unknown_3.hex()}'

    def _npc_dialog_open(self) -> str:
        """
        Start to talk with an NPC, the dialog is open.

        :rtype: str
        :return: Message of this action.
        """
        id_dialog = hex(unpack('<I', self._get_data(4))[0]).zfill(10)
        sub_dialog, = unpack('<c', self._get_data(1))

        return '--> NPC Dialog open' \
               f' | ID {id_dialog}' \
               f' | Sub-dialog {sub_dialog.hex()}'

    def _npc_dialog_next(self) -> str:
        """
        Talking with an NPC, display next dialog.

        :rtype: str
        :return: Message of this action.
        """
        id_dialog = hex(unpack('<I', self._get_data(4))[0]).zfill(10)

        return '--> NPC Dialog next' \
               f' | ID {id_dialog}'

    def _npc_dialog_option_display(self) -> str:
        """
        Talking with an NPC, display new dialog based on the selected option.

        :rtype: str
        :return: Message of this action.
        """
        id_dialog = hex(unpack('<I', self._get_data(4))[0]).zfill(10)
        sub_dialog, = unpack('<c', self._get_data(1))

        return '--> NPC Dialog conversation' \
               f' | ID {id_dialog}' \
               f' | Sub-dialog {sub_dialog.hex()}'

    def _npc_dialog_close(self) -> str:
        """
        Talking with an NPC, the dialog is close.

        :rtype: str
        :return: Message of this action.
        """
        id_dialog = hex(unpack('<I', self._get_data(4))[0]).zfill(10)

        return '--> NPC Dialog close' \
               f' | ID {id_dialog}'

    def _shop_store(self) -> str:
        """
        Open the shop storage.

        :rtype: str
        :return: Message of this action.
        """
        id_dialog = hex(unpack('<I', self._get_data(4))[0]).zfill(10)

        return '--> Shop store' \
               f' | ID {id_dialog}'

    def _shop_buy_item(self) -> str:
        """
        Buy an item.

        :rtype: str
        :return: Message of this action.
        """
        unknown_1, unknown_2, quantity, id_item, = unpack('<ccHH', self._get_data(6))
        unknown_1 = unknown_1.hex()
        unknown_2 = unknown_2.hex()
        id_item = hex(id_item).zfill(6)

        # self.display_info = True
        return '--> Shop buy item' \
               f' | Unknown {unknown_1} {unknown_2}' \
               f' | Quantity {quantity}' \
               f' | ID {id_item}'

    def _shop_shell_item(self) -> str:
        """
        Shell an item.

        :rtype: str
        :return: Message of this action.
        """
        unknown_1, unknown_2, id_item, quantity, = unpack('<ccHH', self._get_data(6))
        unknown_1 = unknown_1.hex()
        unknown_2 = unknown_2.hex()
        id_item = hex(id_item).zfill(6)

        # self.display_info = True
        return '--> Shop shell item' \
               f' | Unknown {unknown_1} {unknown_2}' \
               f' | ID {id_item}' \
               f' | Quantity {quantity}'

    @staticmethod
    def _scenario_change() -> str:
        """
        The scenario was changed.

        :rtype: str
        :return: Message of this action.
        """
        return '--> Scenario change'

    def _connect_server_constant_1(self) -> str:
        """
        The node is communicate with the server constantly.

        :rtype: str
        :return: Message of this action.
        """
        unknown_1, = unpack('<c', self._get_data(1))
        unknown_1 = unknown_1.hex()

        return '--> Communicate with the server [0xbf]' \
               f' | Unknown {unknown_1}'

    @staticmethod
    def _connect_server_constant_2() -> str:
        """
        The node is communicate with the server constantly but not frequently.

        :rtype: str
        :return: Message of this action.
        """
        return '--> Communicate with the server [0x210]'
