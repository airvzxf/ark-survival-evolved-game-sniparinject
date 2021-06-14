#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Unit Test.
"""
from unittest.mock import patch, MagicMock

from core.utility import Utility


class TestUtility:
    @patch('builtins.print')
    def test_print_format_table(self, mock_print: MagicMock):
        # Arrange
        expected_prints_used = 136

        # Act
        Utility.print_format_table()

        # Assert
        assert mock_print.call_count == expected_prints_used

    def test_text_error_format(self):
        # Arrange
        text = 'Is it an error?'
        expected_format = f'\x1b[00;37;41m{text}\x1b[0m'

        # Act
        formatted_code = Utility.text_error_format(text)

        # Assert
        assert formatted_code == expected_format
