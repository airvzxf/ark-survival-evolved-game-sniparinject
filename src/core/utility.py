#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Utilities to handle the parse connection.
"""


class Utility:
    """
    Utilities for the sniffer.
    """

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
            for foreground in fg_color_rage:
                output = ''
                for background in bg_color_rage:
                    text_format = ';'.join([
                        str(style).zfill(2), str(foreground).zfill(2), str(background).zfill(2)
                    ])
                    output += f'\x1b[{text_format}m {text_format} \x1b[0m'
                print(output)

    @staticmethod
    def text_error_format(text: str) -> str:
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

        :rtype: str
        :return: The format code.
        """
        error_code = '00;37;41'

        return f'\x1b[{error_code}m{text}\x1b[0m'
