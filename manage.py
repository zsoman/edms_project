#!/usr/bin/env python
"""This file contains the implementation of test coverage.
"""

# Imports -----------------------------------------------------------------------------------------------------------
import unittest
from os import path

import coverage

# Authorship information  -------------------------------------------------------------------------------------------
__author__ = "Zsolt Bokor Levente"
__copyright__ = "Copyright 2016, Morgan Stanely - Training 360 Project"
__credits__ = "Zsolt Bokor Levente"
__version__ = "1.0.0"
__maintainer__ = "Zsolt Bokor Levente"
__email__ = ["bokor.zsolt5@gmail.com", "bokorzsolt@yahoo.com"]
__status__ = "Development"

# -------------------------------------------------------------------------------------------------------------------

cov = coverage.coverage(branch = True)
cov.start()
tests = unittest.TestLoader().discover('tests/.')
unittest.TextTestRunner(verbosity = 2).run(tests)
cov.stop()
cov.save()
basedir = path.abspath(path.dirname(__file__))
covdir = path.join(basedir, 'coverage')
cov.html_report(directory = covdir)
cov.erase()
