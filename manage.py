import unittest
from os import path

import coverage

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
