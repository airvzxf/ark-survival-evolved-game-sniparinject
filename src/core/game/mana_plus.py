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
        self.display_info = False

        ip_layer = packet.getlayer(IP)
        raw_layer = packet.getlayer(Raw)
        self.raw_data = raw(raw_layer)
        self.raw_data_copy = raw(raw_layer)

        self.node_actions = {
            0x85: self._node_player_move_to,
            0x89: self._node_player_action,
            0x9f: self._node_player_pickup_item,
            0x118: self._node_npc_killed,
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
        id_integer, = unpack('<h', self._get_data(2))

        if id_integer in self.node_actions.keys():
            # self.display_info = True
            self.node_actions.get(id_integer)()
        else:
            self.display_info = True
            if self.display_info:
                id_hex = hex(id_integer)
                print(f'Node:'
                      f' | ID {id_hex}'
                      f' | {self.raw_data.hex()}'
                      )

        self.display_info = False
        if self.display_info and len(self.raw_data_copy) > 0:
            print(f'--> Data'
                  f' | {self.raw_data.hex()}'
                  )

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

    def _node_player_move_to(self) -> None:
        """
        Player moves to specific position.

        :rtype: None
        :return: Nothing
        """
        position_1, position_2, position_3 = unpack('<ccc', self._get_data(3))
        if self.display_info:
            print(f'--> Player move to'
                  f' | {position_1.hex()} {position_2.hex()} {position_3.hex()}'
                  )

    def _node_player_action(self) -> None:
        """
        Player Action.

        :rtype: None
        :return: Nothing
        """
        id_target, = unpack('<c', self._get_data(1))
        unknown_1, unknown_2, unknown_3 = unpack('<ccc', self._get_data(3))
        action_id, = unpack('<B', self._get_data(1))
        action_description = (
            ' = ' + self.node_player_actions.get(action_id)
            if action_id in self.node_player_actions.keys()
            else ''
        )

        self.display_info = True
        if self.display_info:
            print(f'--> Player action'
                  f' | Target {id_target.hex()}'
                  f' | {unknown_1.hex()} {unknown_2.hex()} {unknown_3.hex()}'
                  f' | ID {hex(action_id)}{action_description}'
                  )
        self.display_info = False

    def _node_npc_killed(self) -> None:
        """
        The NPC (Non-Player Character) was killed.

        :rtype: None
        :return: Nothing
        """
        if self.display_info:
            print(f'--> NPC was killed')

    def _node_player_pickup_item(self) -> None:
        """
        Player pick up an item.

        :rtype: None
        :return: Nothing
        """
        self.display_info = True
        action_id, = unpack('<B', self._get_data(1))
        unknown_1, unknown_2, unknown_3 = unpack('<ccc', self._get_data(3))

        print(f'--> Player pick up an item'
              f' | ID {hex(action_id)}'
              f' | {unknown_1.hex()} {unknown_2.hex()} {unknown_3.hex()}'
              )
        self.display_info = False
