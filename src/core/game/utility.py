#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Utilities to handle the parse connection.
"""
from struct import unpack

from core.game.text_style import TextStyle


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

    @staticmethod
    def print_format_table() -> None:
        """
        Prints table with all the text format options.

        :rtype: None
        :return: Nothing.
        """
        style_range = [0, 1, 2, 3, 4, 7, 9, 21]
        fg_color_rage = [30, 31, 32, 33, 34, 35, 36, 37, 90, 91, 92, 93, 94, 95, 96]
        bg_color_rage = [40, 41, 42, 43, 44, 45, 46, 47, 100]
        for style in style_range:
            print()
            print(f'Style: {str(style).zfill(2)}')
            for fg in fg_color_rage:
                s1 = ''
                for bg in bg_color_rage:
                    text_format = ';'.join([
                        str(style).zfill(2), str(fg).zfill(2), str(bg).zfill(2)
                    ])
                    s1 += f'\x1b[{text_format}m {text_format} \x1b[0m'
                print(s1)

    def text_format(self, text: str, style: TextStyle = TextStyle.NORMAL) -> str:
        """
        Prints the text format for host output.

        Style:
        - NORMAL = '0'
        - BOLD = '1'
        - LIGHT = '2'
        - ITALIC = '3'
        - UNDERLINE = '4'
        - SELECTED = '7'
        - STRIKETHROUGH = '9'
        - DOUBLE_UNDERLINE = '21'

        :type text: str
        :param text: The text which will be format.

        :type style: TextStyle
        :param style: Set the style of the text.

        :rtype: str
        :return: The format code.
        """
        format_code = ''

        if style == TextStyle.TITLE:
            format_code += '00;93;'

        if style == TextStyle.NORMAL:
            format_code += '00;30;'

        if style == TextStyle.BOLD:
            format_code += '01;30;'

        if style == TextStyle.LIGHT:
            format_code += '02;30;'

        format_code += '44' if self.request == 'host' else '100'

        return f'\x1b[{format_code}m{text}\x1b[0m'
