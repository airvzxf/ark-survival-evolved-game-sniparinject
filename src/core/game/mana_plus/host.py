#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Manage the host connection of Mana Plus.
"""
from struct import unpack

from core.game.utility import Utility


class ManaPlusHost(Utility):
    """
    Manage the host connection.
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
            0x78: self._npc_info,
            0x7b: self._npc_monster_move_to,
            0x80: self._npc_monster_check,
            0x87: self._player_move,
            0x8a: self._fight,
        }

        self.npc_monster = {
            0x459: 'Pollett',
            0x3fc: 'Fluffy',
            0x445: 'White Smile',
            0x447: 'White Bell',
        }

        super().__init__(self.display_info, self.raw_data_copy)
        # print(self.raw_data.hex())
        self._start()

    def _start(self) -> None:
        """
        Start the parse of the packages.

        :rtype: None
        :return: Nothing.
        """
        if len(self.raw_data_copy) == 0:
            return

        id_package, = unpack('<h', self._get_data(2))
        if id_package in self.actions.keys():
            message = self.actions.get(id_package)()
            self._display_message(message)
        else:
            self.display_info = True
            if self.display_info:
                id_hex = hex(id_package)
                print('HOST'
                      f' | ID {id_hex}'
                      f' | {self.raw_data.hex()}'
                      )
            return

        if len(self.raw_data_copy) > 0:
            self._start()

    def _npc_monster_check(self) -> str:
        """
        Check the specific NPC monster.

        :rtype: str
        :return: Message of this action.
        """
        id_npc, unknown_1, = unpack('<Ic', self._get_data(5))
        id_npc = hex(id_npc).zfill(10)
        unknown_1 = unknown_1.hex()

        return '<-- NPC Monster Check' \
               f' | ID {id_npc}' \
               f' | Unknown {unknown_1}'

    def _player_move(self) -> str:
        """
        Player is moving.

        :rtype: str
        :return: Message of this action.
        """
        (
            id_move, unknown_1, unknown_2, unknown_3,
            unknown_4, unknown_5, unknown_6
        ) = unpack('<Icccccc', self._get_data(10))
        id_move = hex(id_move).zfill(10)
        unknown_1 = unknown_1.hex()
        unknown_2 = unknown_2.hex()
        unknown_3 = unknown_3.hex()
        unknown_4 = unknown_4.hex()
        unknown_5 = unknown_5.hex()
        unknown_6 = unknown_6.hex()

        return '<-- Player move to' \
               f' | ID {id_move}' \
               f' | XY {unknown_1}{unknown_2}{unknown_3}{unknown_4}{unknown_5}' \
               f' | Unknown {unknown_6}'

    def _npc_monster_move_to(self) -> str:
        """
        The NPC Monster is moving to point.

        :rtype: str
        :return: Message of this action.
        """
        (
            monster_id, unknown_2_1, unknown_2_2, unknown_3, unknown_4,
            monster_type, unknown_6, unknown_7, unknown_8, unknown_9,
            unknown_10, hp_current, unknown_12, hp_max, unknown_14,
            unknown_15, unknown_16, unknown_17, unknown_18, unknown_19,
            unknown_20, unknown_21, unknown_22, unknown_23
        ) = unpack('<IccIHHIHIQHHHHIHHcccccIc', self._get_data(58))
        monster_id = hex(monster_id).zfill(10)
        monster_type = self.npc_monster.get(monster_type) or hex(monster_type).zfill(6)
        unknown_2_1 = unknown_2_1.hex()
        unknown_2_2 = unknown_2_2.hex()
        unknown_8 = hex(unknown_8).zfill(10)
        # unknown_16 = hex(unknown_16).zfill(6)
        unknown_17 = unknown_17.hex()
        unknown_18 = unknown_18.hex()
        unknown_19 = unknown_19.hex()
        unknown_20 = unknown_20.hex()
        unknown_21 = unknown_21.hex()
        unknown_23 = unknown_23.hex()

        self.display_info = True
        return '<-- NPC Move' \
               f' | ID {monster_id}' \
               f' | {unknown_2_1} {unknown_2_2}' \
               f' | {unknown_3}' \
               f' {unknown_4}' \
               f' | {monster_type}' \
               f' | {unknown_6} {unknown_7}' \
               f' {unknown_8} {unknown_9}' \
               f' {unknown_10}' \
               f' | HP {hp_current}' \
               f' | {unknown_12}' \
               f' | HP Max {hp_max}' \
               f' | {unknown_14} {unknown_15}' \
               f' | {unknown_16}' \
               f' | XY {unknown_17}{unknown_18}{unknown_19}{unknown_20}{unknown_21}' \
               f' | {unknown_22}' \
               f' {unknown_23}'

    def _fight(self) -> str:
        """
        Fight information.

        :rtype: str
        :return: Message of this action.
        """
        (
            attacker_id, target_id, unknown_1, hp_1, unknown_2, hp_2,
            unknown_3, physical_attack, unknown_5, unknown_6, unknown_7
        ) = unpack('<IIIhhhhhhhc', self._get_data(27))
        attacker_id = hex(attacker_id).zfill(10)
        target_id = hex(target_id).zfill(10)
        unknown_1 = hex(unknown_1).zfill(10)
        physical_attack = str(physical_attack).rjust(4, ' ')
        unknown_7 = unknown_7.hex()

        self.display_info = True
        return '<-- Fight' \
               f' | Attacker {attacker_id}' \
               f' | Target {target_id}' \
               f' | {unknown_1}' \
               f' | ?? {hp_1}' \
               f' | {unknown_2}' \
               f' | ?? {hp_2}' \
               f' | {unknown_3}' \
               f' | Attack {physical_attack}' \
               f' | {unknown_5}' \
               f' | {unknown_6}' \
               f' | {unknown_7}'

    def _npc_info(self) -> str:
        """
        Player is attacking a NPC Monster.

        :rtype: str
        :return: Message of this action.
        """
        (
            target_id, unknown_1_1, unknown_1_2, unknown_2, unknown_3,
            monster_type, unknown_4, unknown_5, hp_current, unknown_6,
            hp_max, unknown_7, unknown_8, unknown_9, position_1, position_2,
            position_3, unknown_10, unknown_11
        ) = unpack('<IccIHHQQHHHIHHcccIc', self._get_data(52))
        target_id = hex(target_id).zfill(10)
        monster_type = self.npc_monster.get(monster_type) or hex(monster_type).zfill(6)
        hp_current = str(hp_current).rjust(4, ' ')
        hp_max = str(hp_max).rjust(4, ' ')
        position_1 = position_1.hex()
        position_2 = position_2.hex()
        position_3 = position_3.hex()
        unknown_11 = unknown_11.hex()
        unknown_1_1 = unknown_1_1.hex()
        unknown_1_2 = unknown_1_2.hex()

        self.display_info = True
        return '<-- NPC Info' \
               f' | ID {target_id}' \
               f' | {unknown_1_1} {unknown_1_2}' \
               f' | {unknown_2}' \
               f' {unknown_3}' \
               f' | {monster_type}' \
               f' | {unknown_4}' \
               f' {unknown_5}' \
               f' | HP {hp_current}' \
               f' | {unknown_6}' \
               f' | HP Max {hp_max}' \
               f' | {unknown_7}' \
               f'  {unknown_8}' \
               f' | {unknown_9}' \
               f' | XY {position_1}{position_2}{position_3}' \
               f' | {unknown_10}' \
               f' {unknown_11}'
