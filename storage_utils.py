#!/usr/bin/env python
"""Various utils for making file-based data management easier.
"""

# Imports -----------------------------------------------------------------------------------------------------------
import logging
import os

# Authorship information  -------------------------------------------------------------------------------------------
__author__ = "Imre Piller"
__copyright__ = "Copyright 2016, Morgan Stanley - Training 360 Project"
__credits__ = __author__
__version__ = "1.0.0"
__maintainer__ = "Zsolt Bokor Levente"
__email__ = ["bokor.zsolt5@gmail.com", "bokorzsolt@yahoo.com"]
__status__ = "Development"

# -------------------------------------------------------------------------------------------------------------------

module_logger = logging.getLogger('repository.storage_utils')


def get_next_id(storage_path):
    """Calculate the next available identifier.

    :param storage_path: The path where to search for the next ID.
    :return: Integer, next ID.
    """
    existing_ids = os.listdir(storage_path)
    integer_ids = []
    for i in existing_ids:
        try:
            current_id = int(i)
            integer_ids.append(current_id)
        except:
            pass
    if len(integer_ids) == 0:
        integer_ids.append(0)
    last_id = max(integer_ids)
    return last_id + 1
