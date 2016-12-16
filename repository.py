"""Repository

The repository is in a dedicated directory. This directory contains the following subdirectories by default:

    documents/  - document data and metadata files
    logs/       - logs of the repository events
    projects/   - project files
    users/      - user metadata files
    paths.ini   - the path of the main parts of the repository
    roles.txt   - user roles

The documents directory contains subdirectories which name is the document identifier.

For document metadata we save them to text files with the same name and .info extension next to the directories.

The paths.ini file contains the (relative or absolute) paths of mentioned subdirectories.

The roles.txt contains the user names and the list of assigned roles.
"""

from datetime import datetime
from os import makedirs, path, utime

from documents import DocumentManager
from iniformat.reader import read_ini_file
from iniformat.writer import write_ini_file
from users import UserManager

ROLES_FILE = 'roles'
PATHS_FILE = 'paths.ini'
FOLDERS_PATH = {'documents': 'documents', 'logs': 'logs', 'projects': 'projects',
                'reports': 'reports', 'users': 'users'}


class Repository(object):
    """Represents the document management system as a repository"""


    def __init__(self, name='Repositiry_1', location=path.join('Repositories', 'repo_1'),
                 roles_file_type='txt'):
        self._document_manager = DocumentManager(location)
        self._user_manager = UserManager(location)
        self._name = name
        self._location = location
        self._metadata_file = path.join(self._location, '{}_metadata.edd'.format(path.basename(self._location)))
        self._paths_file = path.join(self._location, PATHS_FILE)
        self._roles_file_type = roles_file_type
        self.load()


    def load(self):
        """Try to load an existing repository"""
        if path.exists(self._location):
            if path.isdir(self._location):
                self._creation_date = self.read_creation_date()
            else:
                raise ValueError('The repository should be a directory!')
        else:
            self.initialize()


    def initialize(self):
        """Initialize a new repository"""
        makedirs(self._location)
        for name_key, dir_name_value in FOLDERS_PATH.iteritems():
            makedirs(path.join(self._location, dir_name_value))
        role_file_path = reduce(path.join, [self._location, 'users', '{}.{}'.format(ROLES_FILE, self._roles_file_type)])
        with open(role_file_path, 'w') as role_file:
            utime(role_file_path, None)
        self.create_default_path_file()
        self._creation_date = datetime.utcnow()
        self.create_repo_metadata_file(self._creation_date)


    def absolute_path(self):
        if path.isabs(self._location):
            return self._location
        else:
            return path.abspath(self._location)


    def create_default_path_file(self):
        # data = OrderedDict()
        # data['directories']=FOLDERS_PATH
        # data['files']={'repo_main_folder': path.basename(self._location),
        #               'paths': self._paths_file}
        data = {
            'directories': FOLDERS_PATH,
            'files': {'repo_main_folder': path.basename(self._location),
                      'paths': self._paths_file}
        }
        write_ini_file(self._paths_file, data)


    def create_repo_metadata_file(self, date_obj):
        data = {
            'creation_date': {
                'year': date_obj.year,
                'month': date_obj.month,
                'day': date_obj.day,
                'hour': date_obj.hour,
                'minute': date_obj.minute,
                'second': date_obj.second,
                'microsecond': date_obj.microsecond
            }
        }
        write_ini_file(self._metadata_file, data)


    def read_creation_date(self):
        metadata_data = read_ini_file(self._metadata_file)
        return datetime.strptime('{} {} {} {} {} {} {}'.format(
                metadata_data['creation_date']['year'],
                metadata_data['creation_date']['month'],
                metadata_data['creation_date']['day'],
                metadata_data['creation_date']['hour'],
                metadata_data['creation_date']['minute'],
                metadata_data['creation_date']['second'],
                metadata_data['creation_date']['microsecond']
        ), '%Y %m %d %H %M %S %f')

    def import_documents(self, param):
        pass
        # TODO

    def export_documents(self, param, param1):
        pass
        # TODO: only export accepted and public files, if a file is private or not accepted then the hole export is stopped.
