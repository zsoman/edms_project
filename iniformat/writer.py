#!/usr/bin/env python
"""Write data to an ini file
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

module_logger = logging.getLogger('repository.writer')


def write_ini_file(filename, data):
    with open(filename, 'w') as ini_file:
        for section, properties in data.items():
            ini_file.write('[' + section + ']\n')
            for k, v in properties.items():
                ini_file.write(k + '=' + str(v) + "\n")
            ini_file.write('\n')
