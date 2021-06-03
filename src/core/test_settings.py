#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Unit Test.
"""
from unittest.mock import patch

from mock_open import MockOpen
from pytest import raises
from yaml import dump

from core.settings import Settings


class TestSettings:
    def test___init__(self):
        # Arrange
        config_file_expected = 'whatever.txt'
        # Act
        settings = Settings(config_file_expected)
        # Assert
        print(settings.config_file)
        assert False
        # assert settings.config_file == config_file_expected

    def test_get_dictionary(self):
        with patch('builtins.open', MockOpen()):
            # Arrange
            expected = {'Greetings': {'hello': 'world'}, 'Bye': 'Universe'}
            file_name = '/hck/it/yaml-settings.yml'
            with open(file_name, 'w') as handle:
                yaml_content = dump(expected)
                handle.write(yaml_content)
            with open(file_name, 'r'):
                # Act
                settings = Settings(file_name).get_dictionary()
                # Assert
                assert settings == expected

    def test_get_dictionary_not_file_exists(self):
        # Assert
        with raises(FileNotFoundError):
            # Arrange
            file_name = '/hck/it/invisible.yml'
            # Act
            Settings(file_name).get_dictionary()

    def test_get_dictionary_empty_settings(self):
        with patch('builtins.open', MockOpen()):
            # Arrange
            file_name = '/hck/it/yaml-settings.yml'
            with open(file_name, 'r'):
                try:
                    # Act
                    Settings(file_name).get_dictionary()
                except Exception as error:
                    # Assert
                    error_expected = f'Error: Not found settings in the file `{file_name}`.'
                    assert str(error) == error_expected
