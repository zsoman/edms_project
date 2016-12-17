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
from os import makedirs, path, utime, listdir
from shutil import copytree, rmtree

from documents import DocumentManager
from iniformat.reader import read_ini_file
from iniformat.writer import write_ini_file
from users import UserManager

# from users import UserManager

ROLES_FILE = 'roles'
PATHS_FILE = 'paths.ini'
FOLDERS_PATH = {'documents': 'documents', 'logs': 'logs', 'projects': 'projects',
                'reports': 'reports', 'users': 'users'}


class Repository(object):
    """Represents the document management system as a repository"""


    def __init__(self, name='Repositiry_1', location=path.join('Repositories', 'repo_1'), roles_file_type='txt'):
        self._name = name
        self._location = location
        self._metadata_file = path.join(self._location, '{}_metadata.edd'.format(path.basename(self._location)))
        self._paths_file = path.join(self._location, PATHS_FILE)
        self._roles_file_type = roles_file_type
        self.load()
        self._user_manager = UserManager(self._location, self._paths_file)
        self._document_manager = DocumentManager(self._location, self._paths_file)


    # def add_document_manager(self, document_manager):
    #     self._document_manager = document_manager
    #
    #
    # def add_user_manager(self, user_manager):
    #     self._user_manager = user_manager


    def load(self):
        """Try to load an existing repository"""
        if path.exists(self._location):
            if path.isdir(self._location):
                # self._creation_date = self.read_creation_date()
                pass
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


    @classmethod
    def find_all_documents_in_path(cls, from_path):
        all_available_documents = []
        for file_or_folder in listdir(from_path):
            if path.isdir(path.join(from_path, file_or_folder)):
                try:
                    all_available_documents.append(int(file_or_folder))
                except:
                    pass
        return all_available_documents


    def import_documents(self, from_path):
        if path.exists(from_path):
            all_documents = Repository.find_all_documents_in_path(from_path)
            metadata_data = read_ini_file(self._paths_file)
            to_path = path.join(self._location, metadata_data['directories']['documents'])
            if len(all_documents) > 0:
                for document_id in all_documents:
                    new_path = reduce(path.join, [to_path, str(document_id)])
                    old_path = path.join(from_path, str(document_id))
                    copytree(old_path, new_path)
                    try:
                        document_files_existence = self._document_manager.document_files_exist(document_id)
                        for file_name_key, exists_value in document_files_existence.iteritems():
                            if not exists_value:
                                raise RuntimeError(
                                    "The {} file doesn't exists in the {} ID document!".format(file_name_key,
                                                                                               document_id))
                        document = self._document_manager.load_document(document_id)
                        if not isinstance(document.author, list):
                            doc_author = [document.author]
                        else:
                            doc_author = document.author
                        for author in doc_author:
                            _ = self._user_manager.find_user_by_id(author)

                    except Exception as e:
                        rmtree(new_path)
                        raise e
            else:
                raise ValueError("No document to import from the '{}' path!".format(from_path))
        else:
            raise ValueError("The '{}' doesn't exists!".format(from_path))
            # TODO


    def export_documents(self, param, param1):
        pass
        # TODO: only export accepted and public files, if a file is private or not accepted then the hole export is stopped.
