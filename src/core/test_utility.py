#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Unit Test.
"""
from typing import Callable
from unittest.mock import patch, MagicMock, call

from core.text_style import TextStyle
from core.utility import Utility


class TestUtility:
    def test____init__(self):
        # Arrange
        expected_request = 'My request'
        expected_display_info = True
        expected_raw_data = b'\xd5'
        expected_raw_data_copy = b'\xfa'
        expected_actions = {'read': 'my mind'}

        # Act
        utility = Utility(
            expected_request, expected_display_info,
            expected_raw_data, expected_raw_data_copy, expected_actions
        )

        # Assert
        assert utility.request == expected_request
        assert utility.display_info == expected_display_info
        assert utility.raw_data == expected_raw_data
        assert utility.raw_data_copy == expected_raw_data_copy
        assert utility.actions == expected_actions

    @patch('core.utility.unpack')
    def test__start(self, mock_unpack: MagicMock):
        # Arrange
        # Act
        utility = Utility('', False, b'', b'', {})
        utility._start()

        # Assert
        mock_unpack.assert_not_called()

    @patch('core.utility.Utility._display_message')
    def test__start_execute_action(self, mock_display: MagicMock):
        # Arrange
        id_action = 2565  # \x05\x0a
        raw_data_copy = b'\x05\x0a'
        message = 'I need more action!'
        quick_function: Callable[[], str] = lambda: message
        actions = {
            id_action: quick_function
        }

        # Act
        utility = Utility('', False, b'', raw_data_copy, actions)
        utility._start()

        # Assert
        mock_display.assert_called_once_with(message)

    @patch('core.utility.Utility._display_message')
    def test__start_execute_action_recursive(self, mock_display: MagicMock):
        # Arrange
        id_action = 2565  # \x05\x0a
        id_action_recursive = 290  # \x22\x01
        raw_data_copy = b'\x05\x0a\x22\x01'
        message = 'I need more action!'
        message_recursive = 'No more action! Thanks'
        quick_function: Callable[[], str] = lambda: message
        quick_function_recursive: Callable[[], str] = lambda: message_recursive
        actions = {
            id_action: quick_function,
            id_action_recursive: quick_function_recursive,
        }

        # Act
        utility = Utility('', False, b'', raw_data_copy, actions)
        utility._start()

        # Assert
        assert mock_display.call_count == 2
        mock_display.assert_has_calls([
            call(message), call(message_recursive)
        ])

    @patch('builtins.print')
    def test__start_not_execute_action_and_display_info(self, mock_print: MagicMock):
        # Arrange
        id_action = 2565  # \x05\x0a
        raw_data = b'\x05\x0a\x28\x49\x89'
        raw_data_copy = b'\x05\x0a\x28\x49\x89'
        request_type = 'House'
        display_info = True
        expected_message = f'{request_type.upper()}' \
                           f' | ID {hex(id_action)}' \
                           f' | {raw_data_copy.hex()}'

        # Act
        utility = Utility(request_type, display_info, raw_data, raw_data_copy, {})
        utility._start()

        # Assert
        mock_print.assert_called_once_with(expected_message)

    @patch('builtins.print')
    def test__start_not_execute_action_not_display_info(self, mock_print: MagicMock):
        # Arrange
        raw_data_copy = b'\x01\x02\x03'
        display_info = False

        # Act
        utility = Utility('', display_info, b'', raw_data_copy, {})
        utility._start()

        # Assert
        mock_print.assert_not_called()

    def test__get_data(self):
        # Arrange
        raw_data_copy = b'\x01\x02\x03\x04\x05\x06\x07\x08'
        expected_new_data = b'\x01\x02\x03\x04\x05'
        expected_raw_data_copy = b'\x06\x07\x08'

        # Act
        utility = Utility('', False, b'', raw_data_copy, {})
        new_data = utility._get_data(5)

        # Assert
        assert new_data == expected_new_data
        assert utility.raw_data_copy == expected_raw_data_copy

    @patch('builtins.print')
    def test__display_message(self, mock_print: MagicMock):
        # Arrange
        expected_message = 'Hello Drown!'

        # Act
        utility = Utility('', True, b'', b'', {})
        utility._display_message(expected_message)

        # Assert
        mock_print.assert_called_once_with(expected_message)

    @patch('builtins.print')
    def test__display_message_false(self, mock_print: MagicMock):
        # Arrange
        # Act
        utility = Utility('', False, b'', b'', {})
        utility._display_message('whatever')

        # Assert
        mock_print.assert_not_called()

    @patch('builtins.print')
    def test_print_format_table(self, mock_print: MagicMock):
        # Arrange
        expected_prints_used = 136

        # Act
        Utility.print_format_table()

        # Assert
        assert mock_print.call_count == expected_prints_used

    def test_text_format(self):
        # Arrange
        text = 'Bananas and Apples'
        expected_format = f'\x1b[00;30;100m{text}\x1b[0m'

        # Act
        utility = Utility('', False, b'', b'', {})
        formatted_code = utility.text_format(text)

        # Assert
        assert formatted_code == expected_format

    def test_text_format_title(self):
        # Arrange
        text = 'Where I am?'
        expected_format = f'\x1b[00;93;100m{text}\x1b[0m'

        # Act
        utility = Utility('', False, b'', b'', {})
        formatted_code = utility.text_format(text, TextStyle.TITLE)

        # Assert
        assert formatted_code == expected_format

    def test_text_format_bold(self):
        # Arrange
        text = 'Je je je'
        expected_format = f'\x1b[01;30;100m{text}\x1b[0m'

        # Act
        utility = Utility('', False, b'', b'', {})
        formatted_code = utility.text_format(text, TextStyle.BOLD)

        # Assert
        assert formatted_code == expected_format

    def test_text_format_light(self):
        # Arrange
        text = 'My life'
        expected_format = f'\x1b[02;30;100m{text}\x1b[0m'

        # Act
        utility = Utility('', False, b'', b'', {})
        formatted_code = utility.text_format(text, TextStyle.LIGHT)

        # Assert
        assert formatted_code == expected_format

    def test_text_format_host(self):
        # Arrange
        text = 'Check it out!'
        expected_format = f'\x1b[00;30;44m{text}\x1b[0m'

        # Act
        utility = Utility('host', False, b'', b'', {})
        formatted_code = utility.text_format(text)

        # Assert
        assert formatted_code == expected_format
