#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Utilities to handle the parse connection.
"""


class Utility:
    """
    Sniff the Mana Plus game.
    """

    def __init__(self, display_info: bool, raw_data_copy: bytes):
        """
        Initialize the class.

        :type display_info: bool
        :param display_info: Check if it should be display information in console.

        :type raw_data_copy: bytes
        :param raw_data_copy: Copy of the data in bytes.

        :rtype: None
        :return: Nothing.
        """
        self.display_info = display_info
        self.raw_data_copy = raw_data_copy

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
