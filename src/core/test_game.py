#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Unit Test.
"""
from unittest.mock import MagicMock, patch, call

from pytest import raises
from scapy.layers.inet import IP
from scapy.packet import Raw

from core.game import Game
from core.text_style import TextStyle


class TestGame:
    style_error = '\x1b[00;37;41m'
    style_title = '\x1b[00;93;100m'
    style_normal = '\x1b[00;30;100m'
    style_light = '\x1b[00;96;100m'
    style_bold = '\x1b[00;37;100m'
    style_title_host = '\x1b[00;93;44m'
    style_normal_host = '\x1b[00;30;44m'
    style_end = '\x1b[0m'

    def test___init__(self):
        # Arrange
        expected_data = b'\x01\x02\x03'
        expected_packet = IP() / Raw(expected_data)
        expected_settings_path = 'combo-breaker.yml'

        # Act
        game = Game(expected_settings_path, '', expected_packet)

        # Assert
        assert game.settings_path == expected_settings_path
        assert game.raw_data == expected_data
        assert game.raw_data_copy == expected_data
        assert game.request == 'node'
        assert game.display_message is True

    def test___init___host(self):
        # Arrange
        expected_host_ip = '129.185.210.19'
        expected_packet = IP(src=expected_host_ip) / Raw()

        # Act
        game = Game('', expected_host_ip, expected_packet)

        # Assert
        assert game.request == 'host'

    @patch('core.game.Game._parse_packets')
    def test__start(self, mock_parse_packets: MagicMock):
        # Arrange
        # Act
        game = Game('', '', IP() / Raw())
        game.start()

        # Assert
        mock_parse_packets.assert_called_once()

    @patch('builtins.print')
    @patch('core.game.Game._parse_packets')
    def test__start_catch_exception(self, mock_parse_packets: MagicMock, mock_print: MagicMock):
        # Arrange
        expected_error_message = 'ShellBoom!'
        mock_parse_packets.side_effect = FloatingPointError(expected_error_message)

        # Act
        game = Game('', '', IP() / Raw())
        game.start()

        # Assert
        mock_print.assert_has_calls([
            call(f'{self.style_error}Error NODE: {expected_error_message}{self.style_end}'),
            call(f'{self.style_error}Location: Class Game{self.style_end}'),
            call(f'{self.style_error}{self.style_end}'),
            call(),
        ])

    @patch('builtins.print')
    @patch('core.game.Game._parse_packets')
    def test__start_catch_exception_with_location(self, mock_parse_packets: MagicMock, mock_print: MagicMock):
        # Arrange
        expected_error_message = 'zBoom!'
        expected_location = ' -> house() -> bedroom() -> bed()'
        mock_parse_packets.side_effect = LookupError(expected_error_message, expected_location)

        # Act
        game = Game('', '', IP() / Raw())
        game.start()

        # Assert
        mock_print.assert_has_calls([
            call(f'{self.style_error}Error NODE: {expected_error_message}{self.style_end}'),
            call(f'{self.style_error}Location: Class Game{expected_location}{self.style_end}'),
            call(f'{self.style_error}{self.style_end}'),
            call(),
        ])

    def test__extract_exception(self):
        # Arrange
        expected_message = 'KeyholeBoom!'
        exception = ImportError(expected_message)

        # Act
        message, location = Game._extract_exception(exception)

        # Assert
        assert message == expected_message
        assert location == ''

    def test__extract_exception_with_location(self):
        # Arrange
        expected_message = 'AbraKaBoom!'
        expected_location = 'ing'
        exception = BrokenPipeError(expected_message, expected_location)

        # Act
        message, location = Game._extract_exception(exception)

        # Assert
        assert message == expected_message
        assert location == expected_location

    def test__raise_exception(self):
        # Arrange
        expected_message = 'AbcBoom!'
        expected_location = ' with my friends'
        expected_extra_location = 'Play on the table'
        exception = FileNotFoundError(expected_message, expected_location)

        with raises(Exception) as error:
            # Act
            game = Game('', '', IP() / Raw())
            game._raise_exception(exception, expected_extra_location)

        # Assert
        assert error.type == Exception
        assert error.value.args == (expected_message, expected_extra_location + expected_location)

    @patch('builtins.print')
    def test__print_error(self, mock_print: MagicMock):
        # Arrange
        expected_message = 'S.o.S'
        expected_location = 'Phone cabin'
        data = b'\x01\x02\x03'
        expected_data = data.hex()
        packet = IP() / Raw(data)

        # Act
        game = Game('', '', packet)
        game._print_error(expected_message, expected_location)

        # Assert
        mock_print.assert_has_calls([
            call(f'{self.style_error}Error NODE: {expected_message}{self.style_end}'),
            call(f'{self.style_error}Location: {expected_location}{self.style_end}'),
            call(f'{self.style_error}{expected_data}{self.style_end}'),
            call(),
        ])

    @patch('core.game.Game._display_message')
    @patch('core.game.Game._execute_action')
    @patch('core.game.Game._get_settings')
    def test__parse_packets(self,
                            mock__get_settings: MagicMock,
                            mock__execute_action: MagicMock,
                            mock__display_message: MagicMock):
        # Arrange
        data = b'\x09\x00'
        packet = IP() / Raw(data)
        expected_action = {'hello': 'world!'}
        mock__get_settings.return_value = {'actions': {9: expected_action}}

        # Act
        game = Game('', '', packet)
        game._parse_packets()

        # Assert
        mock__execute_action.assert_called_once_with(expected_action)
        mock__display_message.assert_called_once_with(expected_action, mock__execute_action.return_value)

    @patch('core.game.Game._get_settings')
    def test__parse_packets_exception_settings(self, mock__get_settings: MagicMock):
        # Arrange
        expected_error_message = 'HelloBoom!'
        expected_error_location = ' -> _parse_packets()'
        expected_exception = FileNotFoundError(expected_error_message)
        mock__get_settings.side_effect = expected_exception
        packet = IP() / Raw()

        # Act
        game = Game('', '', packet)
        with raises(Exception) as error:
            game._parse_packets()

        # Assert
        assert error.type == Exception
        assert error.value.args == (expected_error_message, expected_error_location)

    @patch('core.game.Game._execute_action')
    @patch('core.game.Game._get_settings')
    def test__parse_packets_exception_execute_action(self,
                                                     mock__get_settings: MagicMock,
                                                     mock__execute_action: MagicMock):
        # Arrange
        expected_error_message = 'BlaBlaBoom!'
        expected_error_location = ' -> _parse_packets()'
        expected_exception = InterruptedError(expected_error_message)
        mock__execute_action.side_effect = expected_exception
        data = b'\x0a\x00'
        packet = IP() / Raw(data)
        mock__get_settings.return_value = {'actions': {10: ''}}

        # Act
        game = Game('', '', packet)
        with raises(Exception) as error:
            game._parse_packets()

        # Assert
        assert error.type == Exception
        assert error.value.args == (expected_error_message, expected_error_location)

    @patch('builtins.print')
    @patch('core.game.Game._get_settings')
    def test__parse_packets_not_action(self, mock__get_settings: MagicMock, mock_print: MagicMock):
        # Arrange
        data = b'\x0a\x00\x12\x34'
        packet = IP() / Raw(data)
        mock__get_settings.return_value = {'actions': {55: ''}}

        # Act
        game = Game('', '', packet)
        game._parse_packets()

        # Assert
        mock_print.assert_has_calls([
            call('NODE | ID 0xa | 1234'),
            call('     |-> 0a001234')
        ])
        mock__get_settings.assert_called_once_with()

    @patch('builtins.print')
    @patch('core.game.Game._get_settings')
    def test__parse_packets_not_action_display_false(self, mock__get_settings: MagicMock, mock_print: MagicMock):
        # Arrange
        data = b'\x0a\x00\x12\x34'
        packet = IP() / Raw(data)
        mock__get_settings.return_value = {'actions': {55: ''}}

        # Act
        game = Game('', '', packet)
        game.display_message = False
        game._parse_packets()

        # Assert
        mock_print.assert_has_calls([
            call('NODE | ID 0xa | 1234'),
            call('     |-> 0a001234')
        ])
        mock__get_settings.assert_called_once_with()

    @patch('core.game.Game._display_message')
    @patch('core.game.Game._execute_action')
    @patch('core.game.Game._get_settings')
    def test__parse_packets_call_itself_recursively(self,
                                                    mock__get_settings: MagicMock,
                                                    mock__execute_action: MagicMock,
                                                    mock__display_message: MagicMock):
        # Arrange
        data = b'\x02\x00\x04\x00'
        packet = IP() / Raw(data)
        mock__get_settings.return_value = {'actions': {2: '', 4: ''}}
        mock__execute_action.return_value = {}
        mock__display_message.return_value = None

        # Act
        game = Game('', '', packet)
        game._parse_packets()

        # Assert
        assert mock__get_settings.call_count == 2

    @patch('core.game.Settings.get_dictionary')
    def test__get_settings(self, mock_settings):
        # Arrange
        expected_action = {52: 'My first action'}
        mock_settings.return_value = {'Game': {'node': expected_action}}

        # Act
        game = Game('', '', IP() / Raw())
        action = game._get_settings()

        # Assert
        assert action == expected_action
        assert game.display_message is True

    @patch('core.game.Settings.get_dictionary')
    def test__get_settings_display_message_false(self, mock_settings):
        # Arrange
        expected_display_message = False
        mock_settings.return_value = {
            'Game': {'node': {'display_message': expected_display_message}}
        }

        # Act
        game = Game('', '', IP() / Raw())
        game._get_settings()

        # Assert
        assert game.display_message is expected_display_message

    @patch('core.game.Settings.get_dictionary')
    def test__get_settings_display_message_true(self, mock_settings):
        # Arrange
        expected_display_message = True
        mock_settings.return_value = {
            'Game': {'node': {'display_message': expected_display_message}}
        }

        # Act
        game = Game('', '', IP() / Raw())
        game._get_settings()

        # Assert
        assert game.display_message is expected_display_message

    @patch('core.game.Settings.get_dictionary')
    def test__get_settings_host(self, mock_settings):
        # Arrange
        expected_action = {23: 'Hosting the web page'}
        mock_settings.return_value = {'Game': {'host': expected_action}}
        host_ip = '246.156.78.192'
        packet = IP(src=host_ip) / Raw()

        # Act
        game = Game('', host_ip, packet)
        action = game._get_settings()

        # Assert
        assert action == expected_action

    @patch('core.game.Settings.get_dictionary')
    def test__get_settings_exception_settings(self, mock_settings):
        # Arrange
        expected_error_message = 'The Game settings are missing.'
        expected_error_location = ' -> Settings(...).get(\'Game\')'
        mock_settings.return_value = {'No Game Key'}

        # Act
        game = Game('', '', IP() / Raw())
        with raises(Exception) as error:
            game._get_settings()

        # Assert
        assert error.type == Exception
        assert error.value.args == (expected_error_message, expected_error_location)

    @patch('core.game.Settings.get_dictionary')
    def test__get_settings_exception_settings_empty(self, mock_settings):
        # Arrange
        expected_error_message = 'The Game settings are missing.'
        expected_error_location = ' -> Settings(...).get(\'Game\')'
        mock_settings.return_value = {'Game': {}}

        # Act
        game = Game('', '', IP() / Raw())
        with raises(Exception) as error:
            game._get_settings()

        # Assert
        assert error.type == Exception
        assert error.value.args == (expected_error_message, expected_error_location)

    @patch('core.game.Game._convert_structs_to_format')
    @patch('core.game.Game._validate_structs')
    @patch('core.game.Game._generate_title_action')
    @patch('core.game.Game._validate_action')
    def test__execute_action(self,
                             mock__validate_action: MagicMock,
                             mock__generate_title_action: MagicMock,
                             mock__validate_structs: MagicMock,
                             mock__convert_structs_to_format: MagicMock):
        # Arrange
        expected_action = {37: 'Mini action'}
        expected_location = ' -> _execute_action()'
        expected_message_one = 'Jumping in '
        expected_message_two = 'my bead'
        expected_structs = ['bye', 'chao']
        mock__generate_title_action.return_value = expected_message_one
        mock__validate_structs.return_value = expected_structs
        mock__convert_structs_to_format.return_value = expected_message_two

        # Act
        game = Game('', '', IP() / Raw())
        message = game._execute_action(expected_action)

        # Assert
        mock__validate_action.assert_called_once_with(expected_action, expected_location)
        mock__generate_title_action.assert_called_once_with(expected_action)
        mock__validate_structs.assert_called_once_with(expected_action)
        mock__convert_structs_to_format.assert_called_once_with(expected_structs, expected_location)
        assert message == expected_message_one + expected_message_two

    @patch('core.game.Game._convert_structs_to_format')
    @patch('core.game.Game._validate_structs')
    @patch('core.game.Game._generate_title_action')
    @patch('core.game.Game._validate_action')
    def test__execute_action_not_structs(self,
                                         mock__validate_action: MagicMock,
                                         mock__generate_title_action: MagicMock,
                                         mock__validate_structs: MagicMock,
                                         mock__convert_structs_to_format: MagicMock):
        # Arrange
        expected_message = 'Darkness my old friend'
        expected_structs = []
        mock__validate_action.return_value = True
        mock__generate_title_action.return_value = expected_message
        mock__validate_structs.return_value = expected_structs
        mock__convert_structs_to_format.return_value = 'I should not appear in the message'

        # Act
        game = Game('', '', IP() / Raw())
        message = game._execute_action({})

        # Assert
        assert message == expected_message

    def test__validate_action(self):
        # Arrange
        # Act
        game = Game('', '', IP() / Raw())
        game._validate_action({985: 'something'}, '')

        # Assert
        assert True

    def test__validate_action_exception_empty_action(self):
        # Arrange
        expected_message = 'The action is empty.'
        expected_location = ' -> I love you baby'

        # Act
        game = Game('', '', IP() / Raw())
        with raises(Exception) as error:
            game._validate_action({}, expected_location)

        # Assert
        assert error.type == Exception
        assert error.value.args == (expected_message, expected_location)

    def test__validate_structs(self):
        # Arrange
        expected_structs = ['pim', 'pom']

        # Act
        structs = Game._validate_structs({'structs': expected_structs})

        # Assert
        assert structs == expected_structs

    def test__validate_structs_not_in_dictionary(self):
        # Arrange
        expected_structs = []

        # Act
        structs = Game._validate_structs({})

        # Assert
        assert structs == expected_structs

    def test__generate_title_action(self):
        # Arrange
        expected_title = 'Mr. Robot'
        expected_message = f'{self.style_title}--> {expected_title}{self.style_end}' \
                           f'{self.style_normal} |{self.style_end}'
        action = {'title': expected_title}

        # Act
        game = Game('', '', IP() / Raw())
        message = game._generate_title_action(action)

        # Assert
        assert message == expected_message

    def test__generate_title_action_host(self):
        # Arrange
        expected_title = 'My name is not, my number is not'
        expected_message = f'{self.style_title_host}<-- {expected_title}{self.style_end}' \
                           f'{self.style_normal_host} |{self.style_end}'
        action = {'title': expected_title}
        host_ip = '129.185.210.19'
        packet = IP(src=host_ip) / Raw()

        # Act
        game = Game('', host_ip, packet)
        message = game._generate_title_action(action)

        # Assert
        assert message == expected_message

    def test__generate_title_action_and_title_not_exists(self):
        # Arrange
        expected_message = f'{self.style_title}--> {self.style_end}' \
                           f'{self.style_normal} |{self.style_end}'
        action = {}

        # Act
        game = Game('', '', IP() / Raw())
        message = game._generate_title_action(action)

        # Assert
        assert message == expected_message

    @patch('core.game.Game._get_struct')
    def test__join_structs(self, mock__get_struct: MagicMock):
        # Arrange
        message_one = 'Heidi'
        message_two = 'Grandpa'
        size_one = 69
        size_two = 4
        size_struct = 51
        expected_formatted_struct = f'{message_one}{message_two}'
        expected_size = size_one + size_two + size_struct
        structs = [
            {'type': 'video tape'},
            {'type': 'audio tape', 'size': size_struct},
        ]
        mock__get_struct.side_effect = [(message_one, size_one), (message_two, size_two)]

        # Act
        game = Game('', '', IP() / Raw())
        message, size = game._join_structs(structs, '')

        # Assert
        assert message == expected_formatted_struct
        assert size == expected_size

    def test__join_structs_exception_missing_type(self):
        # Arrange
        struct = {'Knock-Knock': 'Boo!'}
        structs = [struct]
        expected_message = f'The struct type is missing. Struct -> {struct}.'
        expected_location = ' -> Missing as my dignity()'

        # Act
        game = Game('', '', IP() / Raw())
        with raises(Exception) as error:
            message, size = game._join_structs(structs, expected_location)

        # Assert
        assert error.type == Exception
        assert error.value.args == (expected_message, expected_location)
        # assert message == ''
        # assert size == 0

    @patch('core.game.unpack')
    @patch('core.game.Game._get_struct_name_format')
    @patch('core.game.Game._get_data')
    @patch('core.game.Game._join_structs')
    def test__convert_structs_to_format(self,
                                        mock__join_structs: MagicMock,
                                        mock__get_data: MagicMock,
                                        mock__get_struct_name_format: MagicMock,
                                        mock_unpack: MagicMock):
        # Arrange
        expected_location = 'Bahamas'
        expected_structs_format = '2s'
        expected_structs_size = 16515
        expected_data = b'\x01\x03'
        expected_name = 'Johnny Bravo'
        expected_variable_one = 57
        expected_variable_value_one = 'Kin Kin'
        expected_variable_two = 654
        expected_variable_value_two = 'Kon Kon'
        expected_structs = [
            {
                'name': expected_name,
                'output': {},
                'reference': {expected_variable_one: expected_variable_value_one}
            },
            {
                'output': {},
                'reference': {expected_variable_two: expected_variable_value_two}
            },
        ]
        mock__get_data.return_value = expected_data
        mock__join_structs.return_value = (expected_structs_format, expected_structs_size)
        mock_unpack.return_value = [expected_variable_one, expected_variable_two]
        mock__get_struct_name_format.side_effect = [expected_name, '']

        # Act
        game = Game('', '', IP() / Raw())
        message = game._convert_structs_to_format(expected_structs, expected_location)

        # Assert
        mock__join_structs.assert_called_once_with(expected_structs, expected_location)
        mock__get_data.assert_called_once_with(expected_structs_size)
        mock_unpack.assert_called_once_with(f'<{expected_structs_format}', expected_data)
        assert message == f'{expected_name}' \
                          f'{self.style_light} {expected_variable_value_one}{self.style_end}' \
                          f'{self.style_normal} |{self.style_end}' \
                          f'{self.style_light} {expected_variable_value_two}{self.style_end}' \
                          f'{self.style_normal} |{self.style_end}'

    @patch('core.game.unpack')
    @patch('core.game.Game._get_struct_output_fill_left')
    @patch('core.game.Game._get_struct_output_fill')
    @patch('core.game.Game._get_struct_output_auto_zero_fill')
    @patch('core.game.Game._get_struct_output_zero_fill')
    @patch('core.game.Game._get_struct_output_type')
    @patch('core.game.Game._get_struct_name_format')
    @patch('core.game.Game._get_data')
    @patch('core.game.Game._join_structs')
    def test__convert_structs_to_format_struct_output(self,
                                                      mock__join_structs: MagicMock,
                                                      mock__get_data: MagicMock,
                                                      mock__get_struct_name_format: MagicMock,
                                                      mock_get_one: MagicMock,
                                                      mock_get_two: MagicMock,
                                                      mock_get_three: MagicMock,
                                                      mock_get_four: MagicMock,
                                                      mock_get_five: MagicMock,
                                                      mock_unpack: MagicMock):
        # Arrange
        expected_variable = 86
        expected_get_one = 'A'
        expected_get_two = 'b'
        expected_get_three = 'C'
        expected_get_four = 'd'
        expected_get_five = 'E'
        structs_format = 'I'
        structs_size = 25
        data = b'\x01\x03'
        expected_output = {'octopus': 'octagon'}
        expected_type = 'Typo'
        structs = [
            {
                'output': expected_output,
                'type': expected_type
            }
        ]
        mock__get_data.return_value = data
        mock__join_structs.return_value = (structs_format, structs_size)
        mock_unpack.return_value = [expected_variable]
        mock__get_struct_name_format.return_value = ''
        mock_get_one.return_value = expected_get_one
        mock_get_two.return_value = expected_get_two
        mock_get_three.return_value = expected_get_three
        mock_get_four.return_value = expected_get_four
        mock_get_five.return_value = expected_get_five

        # Act
        game = Game('', '', IP() / Raw())
        message = game._convert_structs_to_format(structs, '')

        # Assert
        mock_get_one.assert_called_once_with(expected_output, expected_variable)
        mock_get_two.assert_called_once_with(expected_output, expected_get_one)
        mock_get_three.assert_called_once_with(expected_output, expected_get_two, expected_type)
        mock_get_four.assert_called_once_with(expected_output, expected_get_three)
        mock_get_five.assert_called_once_with(expected_output, expected_get_four)
        assert message == f'{self.style_light} {expected_get_five}{self.style_end}' \
                          f'{self.style_normal} |{self.style_end}'

    def test__get_struct_name_format(self):
        # Arrange
        expected_name = 'Kardashian'
        struct = {'name': expected_name}

        # Act
        game = Game('', '', IP() / Raw())
        message = game._get_struct_name_format(struct)

        # Assert
        assert message == f'{self.style_bold} {expected_name}{self.style_end}'

    def test__get_struct_name_format_empty_struct(self):
        # Arrange
        struct = {}

        # Act
        game = Game('', '', IP() / Raw())
        message = game._get_struct_name_format(struct)

        # Assert
        assert message == ''

    def test__get_struct_output_type(self):
        # Arrange
        variable = 531
        expected_variable = hex(variable)
        expected_type = 'hex'
        struct = {'type': expected_type}

        # Act
        game = Game('', '', IP() / Raw())
        new_variable = game._get_struct_output_type(struct, variable)

        # Assert
        assert new_variable == expected_variable

    def test__get_struct_output_type_bytes_variable(self):
        # Arrange
        variable = b'\x05\x07\x0b'
        expected_variable = variable.hex()
        expected_type = 'hex'
        struct = {'type': expected_type}

        # Act
        game = Game('', '', IP() / Raw())
        new_variable = game._get_struct_output_type(struct, variable)

        # Assert
        assert new_variable == expected_variable

    def test__get_struct_output_type_without_type(self):
        # Arrange
        expected_variable = 9821
        struct = {}

        # Act
        game = Game('', '', IP() / Raw())
        new_variable = game._get_struct_output_type(struct, expected_variable)

        # Assert
        assert new_variable == expected_variable

    def test__get_struct_output_zero_fill(self):
        # Arrange
        variable = ' How many Zeros?'
        zero_fill_size = len(variable) + 7
        expected_variable = f'0000000{variable}'
        struct = {'zero_fill': zero_fill_size}

        # Act
        game = Game('', '', IP() / Raw())
        new_variable = game._get_struct_output_zero_fill(struct, variable)

        # Assert
        assert new_variable == expected_variable

    def test__get_struct_output_zero_fill_size_zero(self):
        # Arrange
        expected_variable = 'Zero'
        struct = {'zero_fill': 0}

        # Act
        game = Game('', '', IP() / Raw())
        new_variable = game._get_struct_output_zero_fill(struct, expected_variable)

        # Assert
        assert new_variable == expected_variable

    def test__get_struct_output_zero_fill_not_set_in_struct(self):
        # Arrange
        expected_variable = 'I am not here'
        struct = {}

        # Act
        game = Game('', '', IP() / Raw())
        new_variable = game._get_struct_output_zero_fill(struct, expected_variable)

        # Assert
        assert new_variable == expected_variable

    @patch('core.game.Game._get_struct')
    def test__get_struct_output_auto_zero_fill(self, mock__get_struct: MagicMock):
        # Arrange
        variable = ' 123'
        expected_variable = f'00000000000000{variable}'
        struct_type = 'Type me'
        struct_size = 8
        mock__get_struct.return_value = ('', struct_size)
        struct = {'auto_zero_fill': True}

        # Act
        game = Game('', '', IP() / Raw())
        new_variable = game._get_struct_output_auto_zero_fill(struct, variable, struct_type)

        # Assert
        assert new_variable == expected_variable

    def test__get_struct_output_auto_zero_fill_false(self):
        # Arrange
        expected_variable = 'X'
        struct = {'auto_zero_fill': False}

        # Act
        game = Game('', '', IP() / Raw())
        new_variable = game._get_struct_output_auto_zero_fill(struct, expected_variable, 'men')

        # Assert
        assert new_variable == expected_variable

    def test__get_struct_output_auto_zero_fill_none(self):
        # Arrange
        expected_variable = 'X'
        struct = {}

        # Act
        game = Game('', '', IP() / Raw())
        new_variable = game._get_struct_output_auto_zero_fill(struct, expected_variable, 'men')

        # Assert
        assert new_variable == expected_variable

    def test__get_struct_output_fill(self):
        # Arrange
        variable = '0.0'
        expected_variable = f'{variable}     '
        fill_size = len(variable) + 5
        struct = {'fill': fill_size}

        # Act
        game = Game('', '', IP() / Raw())
        new_variable = game._get_struct_output_fill(struct, variable)

        # Assert
        assert new_variable == expected_variable

    def test__get_struct_output_fill_with_size_zero(self):
        # Arrange
        expected_variable = 'Hi'
        struct = {'fill': 0}

        # Act
        game = Game('', '', IP() / Raw())
        new_variable = game._get_struct_output_fill(struct, expected_variable)

        # Assert
        assert new_variable == expected_variable

    def test__get_struct_output_fill_with_non_value(self):
        # Arrange
        expected_variable = 'Hey'
        struct = {}

        # Act
        game = Game('', '', IP() / Raw())
        new_variable = game._get_struct_output_fill(struct, expected_variable)

        # Assert
        assert new_variable == expected_variable

    def test__get_struct_output_fill_left(self):
        # Arrange
        variable = '0.0'
        expected_variable = f'     {variable}'
        fill_size = len(variable) + 5
        struct = {'fill_left': fill_size}

        # Act
        game = Game('', '', IP() / Raw())
        new_variable = game._get_struct_output_fill_left(struct, variable)

        # Assert
        assert new_variable == expected_variable

    def test__get_struct_output_fill_left_with_size_zero(self):
        # Arrange
        expected_variable = 'Hi'
        struct = {'fill': 0}

        # Act
        game = Game('', '', IP() / Raw())
        new_variable = game._get_struct_output_fill_left(struct, expected_variable)

        # Assert
        assert new_variable == expected_variable

    def test__get_struct_output_fill_left_with_non_value(self):
        # Arrange
        expected_variable = 'Hey'
        struct = {}

        # Act
        game = Game('', '', IP() / Raw())
        new_variable = game._get_struct_output_fill_left(struct, expected_variable)

        # Assert
        assert new_variable == expected_variable

    def test__get_struct(self):
        # Arrange
        expected_symbol = 'B'
        expected_size = 1
        struct_type = 'unsigned char'

        # Act
        game = Game('', '', IP() / Raw())
        symbol, size = game._get_struct(struct_type)

        # Assert
        assert symbol == expected_symbol
        assert size == expected_size

    def test__get_struct_with_repeat_count(self):
        # Arrange
        expected_symbol = 'Q'
        expected_size = 8
        struct_type = 'unsigned long'
        repeat_count = 32

        # Act
        game = Game('', '', IP() / Raw())
        symbol, size = game._get_struct(struct_type, repeat_count)

        # Assert
        assert symbol == f'{repeat_count}{expected_symbol}'
        assert size == expected_size

    def test__get_struct_exception_type_error(self):
        # Arrange
        struct_type = 'This type not exists'
        expected_message = f'The struct type ({struct_type}) is not defined in the map of structs.'
        expected_location = ' -> _get_struct()'

        # Act
        game = Game('', '', IP() / Raw())
        with raises(Exception) as error:
            game._get_struct(struct_type)

        # Assert
        assert error.type == Exception
        assert error.value.args == (expected_message, expected_location)

    def test__get_data(self):
        # Arrange
        data = b'\x11\x13\x17\x23'
        size = 2

        # Act
        game = Game('', '', IP() / Raw(data))
        new_data = game._get_data(size)

        # Assert
        assert new_data == data[:size]
        assert game.raw_data_copy == data[size:]
        assert game.raw_data == data

    @patch('builtins.print')
    def test__display_message(self, mock_print: MagicMock):
        # Arrange
        action = {}
        expected_message = 'Ji'

        # Act
        game = Game('', '', IP() / Raw())
        game.display_message = True
        game._display_message(action, expected_message)

        # Assert
        mock_print.assert_called_once_with(expected_message)

    @patch('builtins.print')
    def test__display_message_true_action_true(self, mock_print: MagicMock):
        # Arrange
        action = {'display_message': True}
        expected_message = 'Ai'

        # Act
        game = Game('', '', IP() / Raw())
        game.display_message = True
        game._display_message(action, expected_message)

        # Assert
        mock_print.assert_called_once_with(expected_message)

    @patch('builtins.print')
    def test__display_message_true_action_false(self, mock_print: MagicMock):
        # Arrange
        action = {'display_message': False}
        expected_message = 'Ou'

        # Act
        game = Game('', '', IP() / Raw())
        game.display_message = True
        game._display_message(action, expected_message)

        # Assert
        mock_print.assert_not_called()

    @patch('builtins.print')
    def test__display_message_false_action_true(self, mock_print: MagicMock):
        # Arrange
        action = {'display_message': True}
        expected_message = 'Ou'

        # Act
        game = Game('', '', IP() / Raw())
        game.display_message = False
        game._display_message(action, expected_message)

        # Assert
        mock_print.assert_called_once_with(expected_message)

    @patch('builtins.print')
    def test__display_message_false_action_false(self, mock_print: MagicMock):
        # Arrange
        action = {'display_message': False}
        expected_message = 'Ou'

        # Act
        game = Game('', '', IP() / Raw())
        game.display_message = False
        game._display_message(action, expected_message)

        # Assert
        mock_print.assert_not_called()

    def test_text_format(self):
        # Arrange
        text = 'Conan'
        expected_message = f'{self.style_normal}{text}{self.style_end}'

        # Act
        game = Game('', '', IP() / Raw())
        message = game.text_format(text)

        # Assert
        assert message == expected_message

    def test_text_format_title(self):
        # Arrange
        text = 'Conan'
        expected_message = f'{self.style_title}{text}{self.style_end}'

        # Act
        game = Game('', '', IP() / Raw())
        message = game.text_format(text, TextStyle.TITLE)

        # Assert
        assert message == expected_message

    def test_text_format_bold(self):
        # Arrange
        text = 'Conan'
        expected_message = f'{self.style_bold}{text}{self.style_end}'

        # Act
        game = Game('', '', IP() / Raw())
        message = game.text_format(text, TextStyle.BOLD)

        # Assert
        assert message == expected_message

    def test_text_format_light(self):
        # Arrange
        text = 'Conan'
        expected_message = f'{self.style_light}{text}{self.style_end}'

        # Act
        game = Game('', '', IP() / Raw())
        message = game.text_format(text, TextStyle.LIGHT)

        # Assert
        assert message == expected_message

    def test_text_format_host(self):
        # Arrange
        text = 'Conan'
        expected_message = f'{self.style_normal_host}{text}{self.style_end}'

        # Act
        game = Game('', '', IP() / Raw())
        game.request = 'host'
        message = game.text_format(text)

        # Assert
        assert message == expected_message
