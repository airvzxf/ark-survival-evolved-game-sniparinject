#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Given a YAML file it get the settings and return a dictionary with them.
"""
from yaml import load, FullLoader


# pylint: disable=too-few-public-methods
class Settings:
    """
    Parse the configuration file and return the settings.
    """

    def __init__(self, config_file: str) -> None:
        """
        Parse the configuration file and return the settings.

        :type config_file: str
        :param config_file: Configuration file in YAML format.

        :rtype: None
        :return: Nothing.
        """
        self.config_file = config_file

    def get_dictionary(self) -> dict:
        """
        Return the settings as a Python's dictionary.

        :rtype: dict
        :return: The settings for Python usage.
        """
        with open(self.config_file) as file:
            settings = load(file, Loader=FullLoader)

            if not settings:
                raise Exception(f'Error: Not found settings in the file `{self.config_file}`.')

            return settings
