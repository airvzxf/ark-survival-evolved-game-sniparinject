#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Enumeration with the style of the text format.
"""
from enum import Enum


class TextStyle(Enum):
    """
    Enumeration with the text styles.
    """
    TITLE = 1
    NORMAL = 2
    BOLD = 3
    LIGHT = 4
    ERROR = 5
