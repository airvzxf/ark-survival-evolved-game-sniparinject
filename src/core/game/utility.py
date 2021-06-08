#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Utilities to handle the parse connection.
"""
from struct import unpack


class Utility:
    """
    Sniff the Mana Plus game.
    """

    def __init__(self, request: str, display_info: bool, raw_data: bytes, raw_data_copy: bytes, actions: dict):
        """
        Initialize the class.

        :type request: str
        :param request: Type of request: Host or Node.

        :type display_info: bool
        :param display_info: Check if it should be display information in console.

        :type raw_data: bytes
        :param raw_data: Pure data in bytes.

        :type raw_data_copy: bytes
        :param raw_data_copy: Copy of the data in bytes.

        :type actions: dict
        :param actions: Matrix with the relationship between the ID package and the function.

        :rtype: None
        :return: Nothing.
        """
        self.display_info = display_info
        self.raw_data = raw_data
        self.raw_data_copy = raw_data_copy
        self.actions = actions
        self.request = request

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
                print(f'{self.request.upper()}'
                      f' | ID {id_hex}'
                      f' | {self.raw_data.hex()}'
                      )
            return

        if len(self.raw_data_copy) > 0:
            self._start()

    def _get_data(self, size: int) -> bytes:
        """
        Split the data in two parts.
        The first one is returned the second is updated in the referenced variable.

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
