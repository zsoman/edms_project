import os
import shutil
import unittest

from iniformat.reader import read_ini_file
from repository import Repository


class TestRepository(unittest.TestCase):
    """Test the repository class"""


    def test_empty_repository_creation(self):
        Repository('Empty', '/tmp/test_repo')
        self.assertTrue(os.path.isdir('/tmp/test_repo/documents'))
        self.assertTrue(os.path.isdir('/tmp/test_repo/projects'))
        self.assertTrue(os.path.isdir('/tmp/test_repo/logs'))
        self.assertTrue(os.path.isdir('/tmp/test_repo/users'))
        self.assertTrue(os.path.exists('/tmp/test_repo/paths.ini'))
        self.assertTrue(os.path.exists('/tmp/test_repo/users/roles.txt'))

        # THIS IS WRONG!!! You can't predict the order of a dictionary => you can't test an INI file by line!
        # with open('/tmp/test_repo/paths.ini') as path_file:
        #     self.assertEqual(path_file.readline().rstrip('\n'), '[directories]')
        #     self.assertEqual(path_file.readline().rstrip('\n'), 'documents=documents')
        #     self.assertEqual(path_file.readline().rstrip('\n'), 'logs=logs')
        #     self.assertEqual(path_file.readline().rstrip('\n'), 'projects=projects')
        #     self.assertEqual(path_file.readline().rstrip('\n'), 'users=users')

        metadata_file = read_ini_file('/tmp/test_repo/paths.ini')
        self.assertEqual(metadata_file['directories']['documents'], 'documents')
        self.assertEqual(metadata_file['directories']['logs'], 'logs')
        self.assertEqual(metadata_file['directories']['projects'], 'projects')
        self.assertEqual(metadata_file['directories']['users'], 'users')
        shutil.rmtree('/tmp/test_repo')
