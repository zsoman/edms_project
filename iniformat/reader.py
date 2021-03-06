#!/usr/bin/env python
""" Read data from an ini file.

 - The ini file can contains sections and properties.
 - The section and property names are arbitrary without restrictions.
 - The section denoted by leading [ and trailing ] as the first non-whitespace characters.
 - The duplicated section or property definition causes error.
"""

# Imports -----------------------------------------------------------------------------------------------------------
import logging

# Authorship information  -------------------------------------------------------------------------------------------
__author__ = "Imre Piller"
__copyright__ = "Copyright 2016, Morgan Stanley - Training 360 Project"
__credits__ = __author__
__version__ = "1.0.0"
__maintainer__ = "Zsolt Bokor Levente"
__email__ = ["bokor.zsolt5@gmail.com", "bokorzsolt@yahoo.com"]
__status__ = "Development"

# -------------------------------------------------------------------------------------------------------------------

module_logger = logging.getLogger('repository.reader')


def read_ini_file(path):
    content = {}
    section_name = ''
    with open(path) as ini_file:
        for line in ini_file:
            line = line.rstrip('\n')
            if is_section_header(line):
                section_name = get_section_name(line)
                content[section_name] = {}
            elif is_property(line):
                key, value = get_property(line)
                content[section_name][key] = value
    return content


def is_section_header(line):
    if len(line) >= 2 and line[0] == '[' and line[-1] == ']':
        return True
    return False


def get_section_name(line):
    return line[1:-1]


def is_property(line):
    if '=' in line:
        return True
    return False


def get_property(line):
    splitted = line.split('=')
    if len(splitted) == 2:
        key = splitted[0].strip()
        value = splitted[1].strip()
        return (key, value)
    else:
        raise ValueError('Invalid property line!')
