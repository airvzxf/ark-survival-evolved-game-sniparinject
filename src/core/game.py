#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Parse the game data.
"""
from struct import unpack

from scapy.compat import raw
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether
from scapy.packet import Raw

from core.settings import Settings
from core.text_style import TextStyle
from core.utility import Utility


class Game:
    """
    Parse the game data.
    """

    def __init__(self, settings_path: str, host_ip: str, packet: Ether):
        """
        Parse the game data.

        :type settings_path: str
        :param settings_path: The file path with all the settings.

        :type host_ip: str
        :param host_ip: IP of the host means source or destination.

        :type packet: Ether
        :param packet: Ethernet packet.

        :rtype: None
        :return: Nothing.
        """
        ip_layer = packet.getlayer(IP)
        raw_layer = packet.getlayer(Raw)
        self.raw_data = raw(raw_layer)
        self.raw_data_copy = raw(raw_layer)
        self.settings_path = settings_path
        self.request = 'node'
        self.display_message = True

        if host_ip == ip_layer.src:
            self.request = 'host'

    # pylint: disable=broad-except
    def start(self) -> None:
        """
        Start to process the network packets sniffer and parse.

        :rtype: None
        :return: Nothing.
        """
        try:
            self._parse_packets()
        except Exception as error:
            error_message, error_location = self._extract_exception(error)
            error_location = f'Class Game{error_location}'
            self._print_error(error_message, error_location)
            return

    @staticmethod
    def _extract_exception(error: Exception) -> tuple[str, str]:
        """
        Extract the information from the exception error.

        :type error: Exception
        :param error: Error exception.

        :rtype: tuple[str, str]
        :return: Return the the error message and the location.
        """
        location = ''

        if len(error.args) == 2:
            message = error.args[0]
            location += error.args[1]
        else:
            message = str(error)

        return message, location

    def _raise_exception(self, error: Exception, location: str = '') -> None:
        """
        Raise an exception taking the information from the error.

        :type error: Exception
        :param error: Error exception.

        :type location: str
        :param location: The cascade classes and functions where the error occurred.

        :rtype: tuple[str, str]
        :return: Return the the error message and the location.
        """
        message, extracted_location = self._extract_exception(error)
        full_location = f'{location}{extracted_location}'
        raise Exception(message, full_location)

    def _print_error(self, error: str, location: str) -> None:
        """
        Print the error.

        :type error: str
        :param error: Error message.

        :type location: str
        :param location: The cascade classes and functions where the error occurred.

        :rtype: None
        :return: Nothing.
        """
        message = Utility.text_error_format(f'Error {self.request.upper()}: {error}')
        location = Utility.text_error_format(f'Location: {location}')
        data = Utility.text_error_format(f'{self.raw_data.hex()}')
        print(message)
        print(location)
        print(data)
        print()

    # pylint: disable=broad-except
    def _parse_packets(self) -> None:
        """
        Start the parse of the packets.

        :rtype: None
        :return: Nothing.
        """
        exception_location = ' -> _parse_packets()'
        settings = {}
        try:
            settings = self._get_settings()
        except Exception as error:
            self._raise_exception(error, exception_location)

        packet_id, = unpack('<h', self._get_data(2))
        actions = settings.get('actions') or {}
        if packet_id in actions.keys():
            action = actions.get(packet_id) or {}
            message = ''
            try:
                message = self._execute_action(action)
            except Exception as error:
                self._raise_exception(error, exception_location)
            self._display_message(action, message)
        else:
            if self.display_message:
                print(f'{self.request.upper()}'
                      f' | ID {hex(packet_id)}'
                      f' | {self.raw_data_copy.hex()}')
                print(f'     |-> {self.raw_data.hex()}')
            return

        if len(self.raw_data_copy) > 0:
            self._parse_packets()

    # noinspection PyBroadException
    def _get_settings(self) -> dict:
        """
        Validate and return the settings dictionary.

        :rtype: dict
        :return: The actions with the settings.
        """
        settings_exception = Exception('The Game settings are missing.',
                                       ' -> Settings(...).get(\'Game\')')

        general_settings = {}
        try:
            general_settings = Settings(self.settings_path).get_dictionary().get('Game') or {}
        except Exception:
            self._raise_exception(settings_exception)

        if len(general_settings) < 1:
            self._raise_exception(settings_exception)

        if self.request == 'host':
            settings = general_settings.get('host') or {}
        else:
            settings = general_settings.get('node') or {}

        self.display_message: bool = settings.get('display_message') is not (None or False)

        return settings

    def _execute_action(self, action: dict) -> str:
        """
        Create an output given the action settings.

        :type action: dict
        :param action: Properties of the actions.

        :rtype: str
        :return: Message of this action.
        """
        exception_location = ' -> _execute_action()'

        self._validate_action(action, exception_location)
        message = self._generate_title_action(action)

        structs = self._validate_structs(action)
        if not structs:
            return message

        message += self._convert_structs_to_format(structs, exception_location)

        return message

    def _validate_action(self, action: dict, exception_location: str) -> None:
        """
        Validate the action.

        :type action: dict
        :param action: Properties of the actions.

        :type exception_location: dict
        :param exception_location: The function where the exception occurred.

        :rtype: None
        :return: Nothing
        """
        if len(action.keys()) == 0:
            self._raise_exception(
                Exception('The action is empty.', exception_location)
            )

    @staticmethod
    def _validate_structs(action: dict) -> list:
        """
        Validate the structs.

        :type action: dict
        :param action: Properties of the actions.

        :rtype: list
        :return: The list of the structs.
        """
        return action.get('structs') or []

    def _generate_title_action(self, action: dict) -> str:
        """
        Generate the title of the action.

        :type action: dict
        :param action: Properties of the actions.

        :rtype: str
        :return: Message of this action.
        """
        title = action.get('title') or ''
        direction = '<--' if self.request == 'host' else '-->'
        message = self.text_format(f'{direction} {title}', TextStyle.TITLE)
        message += self.text_format(' |')

        return message

    def _join_structs(self, structs: list, exception_location: str) -> tuple[str, int]:
        """
        Join all the structs and return useful information.

        :type structs: list
        :param structs: List with the structs information.

        :type exception_location: dict
        :param exception_location: The function where the exception occurred.

        :rtype: tuple[str, int]
        :return: Return the formatted message and the size in bytes.
        """
        formatted_struct = ''
        size = 0
        for struct in structs:
            struct_type_setting = struct.get('type') or None
            if struct_type_setting is None:
                self._raise_exception(
                    Exception(
                        f'The struct type is missing. Struct -> {struct}.',
                        exception_location)
                )

            struct_repeat_count = int(struct.get('size') or 0)
            if struct_repeat_count != 0:
                size += struct_repeat_count

            struct_type, struct_size = self._get_struct(struct_type_setting, struct_repeat_count)
            formatted_struct += struct_type
            size += struct_size

        return formatted_struct, size

    def _convert_structs_to_format(self, structs: list, exception_location: str) -> str:
        """
        Convert the structs into message format.

        :type structs: list
        :param structs: The list with the structs.

        :type exception_location: dict
        :param exception_location: The function where the exception occurred.

        :rtype: str
        :return: Message of this action.
        """
        message = ''
        structs_format, structs_size = self._join_structs(structs, exception_location)

        for index, variable in enumerate(
                unpack(f'<{structs_format}', self._get_data(structs_size))):
            struct: dict = structs[index]
            message += self._get_struct_name_format(struct)

            struct_output: dict = struct.get('output') or None
            struct_reference: dict = struct.get('reference') or None
            if struct_reference and variable in struct_reference:
                variable = struct_reference[variable]
                struct_output = {}

            if struct_output:
                variable = self._get_struct_output_type(struct_output, variable)
                variable = self._get_struct_output_zero_fill(struct_output, variable)
                variable = self._get_struct_output_auto_zero_fill(
                    struct_output, variable, struct.get('type'))
                variable = self._get_struct_output_fill(struct_output, variable)
                variable = self._get_struct_output_fill_left(struct_output, variable)

            message += self.text_format(f' {variable}', TextStyle.LIGHT)
            message += self.text_format(' |')

        return message

    def _get_struct_name_format(self, struct: dict) -> str:
        """
        Get the struct name with format.

        :type struct: dict
        :param struct: The struct information of the output.

        :rtype: str
        :return: Message with format.
        """
        struct_name: str = struct.get('name') or None
        if struct_name:
            return self.text_format(f' {struct_name}', TextStyle.BOLD)

        return ''

    @staticmethod
    def _get_struct_output_type(struct: dict, variable: any) -> any:
        """
        Get the struct output type with format.

        :type struct: dict
        :param struct: The struct information of the output.

        :type struct: any
        :param struct: The variable which will be replaced.

        :rtype: Any
        :return: Variable with the format.
        """
        struct_output_type: str = struct.get('type') or None
        if struct_output_type and struct_output_type.lower() == 'hex':
            return variable.hex() if isinstance(variable, bytes) else hex(variable)

        return variable

    @staticmethod
    def _get_struct_output_zero_fill(struct: dict, variable: any) -> any:
        """
        Get the struct output of zero fill with format.

        :type struct: dict
        :param struct: The struct information of the output.

        :type struct: any
        :param struct: The variable which will be replaced.

        :rtype: Any
        :return: Variable with the format.
        """
        output_zero_fill: int = struct.get('zero_fill') or 0
        if output_zero_fill > 0 and isinstance(variable, str):
            return variable.zfill(output_zero_fill)

        return variable

    def _get_struct_output_auto_zero_fill(self, struct: dict,
                                          variable: any, struct_type: str) -> any:
        """
        Get the struct output of auto zero fill with format.

        :type struct: dict
        :param struct: The struct information of the output.

        :type struct: any
        :param struct: The variable which will be replaced.

        :type struct_type: str
        :param struct_type: The type of the struct.

        :rtype: Any
        :return: Variable with the format.
        """
        output_auto_zero_fill: bool = struct.get('auto_zero_fill') or False
        if output_auto_zero_fill and isinstance(variable, str):
            struct_type: str = struct_type or ''
            _, struct_size = self._get_struct(struct_type)
            struct_size *= 2
            struct_size += 2
            return variable.zfill(struct_size)

        return variable

    @staticmethod
    def _get_struct_output_fill(struct: dict, variable: any) -> any:
        """
        Get the struct output with fill left format.

        :type struct: dict
        :param struct: The struct information of the output.

        :type struct: any
        :param struct: The variable which will be replaced.

        :rtype: Any
        :return: Variable with the format.
        """
        output_fill: int = struct.get('fill') or 0
        if output_fill > 0:
            return str(variable).ljust(output_fill)

        return variable

    @staticmethod
    def _get_struct_output_fill_left(struct: dict, variable: any) -> any:
        """
        Get the struct output with fill left format.

        :type struct: dict
        :param struct: The struct information of the output.

        :type struct: any
        :param struct: The variable which will be replaced.

        :rtype: Any
        :return: Variable with the format.
        """
        output_fill_left: int = struct.get('fill_left') or 0
        if output_fill_left > 0:
            variable = str(variable).rjust(output_fill_left)

        return variable

    def _get_struct(self, struct_type: str, repeat_count: int = 1) -> tuple[str, int]:
        """
        Map of the structs with the correlated symbol.

        :type struct_type: str
        :param struct_type: Full name description.

        :type repeat_count: int
        :param repeat_count: Times that the symbol will repeat.

        :rtype: tuple[str, int]
        :return: The struct symbol and its size.
        """
        exception_location = ' -> _get_struct()'
        structs = {
            'char': ('c', 1),
            'signed char': ('b', 1),
            'unsigned char': ('B', 1),
            'bool': ('?', 1),
            'short': ('h', 2),
            'unsigned short': ('H', 2),
            'int': ('i', 4),
            'unsigned int': ('I', 4),
            'long': ('q', 8),
            'unsigned long': ('Q', 8),
            'half precision': ('e', 2),
            'float': ('f', 4),
            'double': ('d', 6),
            'chars': ('s', 0),
        }

        symbol = ''
        size = 0
        try:
            symbol, size = structs.get(struct_type.lower())
        except TypeError:
            self._raise_exception(
                Exception(
                    f'The struct type ({struct_type}) is not defined in the map of structs.',
                    exception_location)
            )

        if repeat_count > 1:
            symbol = f'{repeat_count}{symbol}'

        return symbol, size

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

    def _display_message(self, action: dict, message: str) -> None:
        """
        Print message in the console.

        :type message: str
        :param message: Size of data which will split.

        :rtype: None
        :return: Nothing.
        """
        action_display_info = action.get('display_message')

        if self.display_message and action_display_info is None:
            print(message)
            return

        if action_display_info:
            print(message)
            return

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
            format_code += '00;37;'

        if style == TextStyle.LIGHT:
            format_code += '00;96;'

        format_code += '44' if self.request == 'host' else '100'

        return f'\x1b[{format_code}m{text}\x1b[0m'
