#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Sniff the Mana Plus game.
https://archlinux.org/packages/community/x86_64/manaplus/
"""
from struct import unpack

from scapy.compat import raw
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether
from scapy.packet import Raw


class ManaPlus:
    """
    Sniff the Mana Plus game.
    """

    def __init__(self, host: str, packet: Ether):
        """
        Initialize the class.

        :type host: str
        :param host: IP of the host means source or destination.

        :type packet: Ether
        :param packet: Ethernet packet.

        :rtype: None
        :return: Nothing.
        """
        self.host = host
        self.packet = packet
        self.display_info = True

        ip_layer = packet.getlayer(IP)
        raw_layer = packet.getlayer(Raw)
        self.raw_data = raw(raw_layer)
        self.raw_data_copy = raw(raw_layer)

        self.node_actions = {
            0x7d: self._node_scenario_change,
            0x85: self._node_player_move_to,
            0x89: self._node_player_action,
            0x90: self._node_npc_dialog_open,
            0x94: self._node_character_visible,
            0x9b: self._node_unknown_1_npc_monster_or_dropped_items,
            0x9f: self._node_player_pickup_item,
            0xb8: self._node_npc_dialog_option_display,
            0xb9: self._node_npc_dialog_next,
            0xbf: self._node_connect_server_constant_1,
            0xc5: self._node_shop_store,
            0xc8: self._node_shop_buy_item,
            0xc9: self._node_shop_shell_item,
            0x118: self._node_npc_killed,
            0x146: self._node_npc_dialog_close,
            0x210: self._node_connect_server_constant_2,
        }

        self.node_player_actions = {
            0x2: 'Sit down',
            0x3: 'Stan up',
            0x7: 'Attack NPC',
        }

        source = ip_layer.src
        if host == source:
            # self._from_host()
            pass
        else:
            self._from_node()

    def _from_host(self) -> None:
        """
        The package is coming from the host.

        :rtype: None
        :return: Nothing.
        """
        print(f'Host: {self.raw_data.hex()}')

    def _from_node(self) -> None:
        """
        The package is coming from the node.

        :rtype: None
        :return: Nothing.
        """
        if len(self.raw_data_copy) == 0:
            return

        id_package, = unpack('<h', self._get_data(2))
        if id_package in self.node_actions.keys():
            message = self.node_actions.get(id_package)()
            self._display_message(message)
        else:
            self.display_info = True
            if self.display_info:
                id_hex = hex(id_package)
                print('***'
                      f' | ID {id_hex}'
                      f' | {self.raw_data.hex()}'
                      )
            return

        if len(self.raw_data_copy) > 0:
            self._from_node()

    def _get_data(self, size: int) -> bytes:
        """
        Split the data in two parts.
        The first one is returned the second is updated in the global data.

        :type size: int
        :param size: Size of data which will split.

        :rtype: bytes
        :return: The split data.
        """
        data = self.raw_data_copy[:size]
        self.raw_data_copy = self.raw_data_copy[size:]

        return data

    def _display_message(self, message: str) -> None:
        """
        Print message in the console.

        :type message: str
        :param message: Size of data which will split.

        :rtype: None
        :return: Nothing.
        """
        if self.display_info:
            print(message)

    def _node_player_move_to(self) -> str:
        """
        Player moves to specific position.

        :rtype: str
        :return: Message of this action.
        """
        position_1, position_2, position_3 = unpack('<ccc', self._get_data(3))

        return '--> Player move to' \
               f' | {position_1.hex()} {position_2.hex()} {position_3.hex()}'

    def _node_player_action(self) -> str:
        """
        Player Action.

        :rtype: str
        :return: Message of this action.
        """
        id_target = hex(unpack('<I', self._get_data(4))[0]).zfill(10)
        action_id, = unpack('<B', self._get_data(1))
        action_description = (
            ' = ' + self.node_player_actions.get(action_id)
            if action_id in self.node_player_actions.keys()
            else ''
        )

        self.display_info = True
        return '--> Player action' \
               f' | Target {id_target}' \
               f' | ID {hex(action_id)}{action_description}'

    @staticmethod
    def _node_npc_killed() -> str:
        """
        The NPC (Non-Player Character) was killed.

        :rtype: str
        :return: Message of this action.
        """
        return '--> NPC was killed'

    def _node_player_pickup_item(self) -> str:
        """
        Player pick up an item.

        :rtype: str
        :return: Message of this action.
        """
        action_id, = unpack('<B', self._get_data(1))
        unknown_1, unknown_2, unknown_3 = unpack('<ccc', self._get_data(3))

        self.display_info = True
        return '--> Player pick up an item' \
               f' | ID {hex(action_id)}' \
               f' | Unknown {unknown_1.hex()} {unknown_2.hex()} {unknown_3.hex()}'

    def _node_character_visible(self) -> str:
        """
        The character is visible for me.

        :rtype: str
        :return: Message of this action.
        """
        id_target = hex(unpack('<I', self._get_data(4))[0]).zfill(10)

        return '--> Character visible' \
               f' | ID {id_target}'

    def _node_unknown_1_npc_monster_or_dropped_items(self) -> str:
        """
        Something is sending to the server related to the NPC Monsters or dropped items.

        :rtype: str
        :return: Message of this action.
        """
        unknown_1, unknown_2, unknown_3 = unpack('<ccc', self._get_data(3))

        self.display_info = True
        return '--> Unknown 1 --> Related NPC Monsters or dropped Items' \
               f' | Unknown {unknown_1.hex()} {unknown_2.hex()} {unknown_3.hex()}'

    def _node_npc_dialog_open(self) -> str:
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

    def _node_npc_dialog_next(self) -> str:
        """
        Talking with an NPC, display next dialog.

        :rtype: str
        :return: Message of this action.
        """
        id_dialog = hex(unpack('<I', self._get_data(4))[0]).zfill(10)

        return '--> NPC Dialog next' \
               f' | ID {id_dialog}'

    def _node_npc_dialog_option_display(self) -> str:
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

    def _node_npc_dialog_close(self) -> str:
        """
        Talking with an NPC, the dialog is close.

        :rtype: str
        :return: Message of this action.
        """
        id_dialog = hex(unpack('<I', self._get_data(4))[0]).zfill(10)

        return '--> NPC Dialog close' \
               f' | ID {id_dialog}'

    def _node_shop_store(self) -> str:
        """
        Open the shop storage.

        :rtype: str
        :return: Message of this action.
        """
        id_dialog = hex(unpack('<I', self._get_data(4))[0]).zfill(10)

        return '--> Shop store' \
               f' | ID {id_dialog}'

    def _node_shop_buy_item(self) -> str:
        """
        Buy an item.

        :rtype: str
        :return: Message of this action.
        """
        unknown_1, unknown_2, quantity, id_item, = unpack('<ccHH', self._get_data(6))
        unknown_1 = unknown_1.hex()
        unknown_2 = unknown_2.hex()
        id_item = hex(id_item).zfill(6)

        self.display_info = True
        return '--> Shop buy item' \
               f' | Unknown {unknown_1} {unknown_2}' \
               f' | Quantity {quantity}' \
               f' | ID {id_item}'

    def _node_shop_shell_item(self) -> str:
        """
        Shell an item.

        :rtype: str
        :return: Message of this action.
        """
        unknown_1, unknown_2, id_item, quantity, = unpack('<ccHH', self._get_data(6))
        unknown_1 = unknown_1.hex()
        unknown_2 = unknown_2.hex()
        id_item = hex(id_item).zfill(6)

        self.display_info = True
        return '--> Shop shell item' \
               f' | Unknown {unknown_1} {unknown_2}' \
               f' | ID {id_item}' \
               f' | Quantity {quantity}'

    @staticmethod
    def _node_scenario_change() -> str:
        """
        The scenario was changed.

        :rtype: str
        :return: Message of this action.
        """
        return '--> Scenario change'

    def _node_connect_server_constant_1(self) -> str:
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
    def _node_connect_server_constant_2() -> str:
        """
        The node is communicate with the server constantly but not frequently.

        :rtype: str
        :return: Message of this action.
        """
        return '--> Communicate with the server [0x210]'
