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

import webbrowser
from datetime import datetime
from os import makedirs, path, utime, listdir, remove
from shutil import copytree, rmtree, copy2, make_archive
from zipfile import ZipFile

import schedule
from jinja2 import Environment, FileSystemLoader

from documents import DocumentManager
from iniformat.reader import read_ini_file
from iniformat.writer import write_ini_file
from users import UserManager

# from users import UserManager

ROLES_FILE = 'roles'
PATHS_FILE = 'paths.ini'
FOLDERS_PATH = {'documents': 'documents', 'logs': 'logs', 'projects': 'projects',
                'reports': 'reports', 'users': 'users'}
BACKUP_FREQUENCY = 7


class Repository(object):
    """Represents the document management system as a repository"""

    def __init__(self, name = 'Repository', location = path.join('Repositories', 'repo_1'), roles_file_type = 'txt'):
        self._name = name
        self._location = location
        self._metadata_file = path.join(self._location, '{}_metadata.edd'.format(path.basename(name)))
        self._paths_file = path.join(self._location, PATHS_FILE)
        self._roles_file_type = roles_file_type
        self._user_manager = UserManager(self._location, self._paths_file)
        self._document_manager = DocumentManager(self._location, self._paths_file)
        self.load()
        schedule.every(BACKUP_FREQUENCY).day.at('4:00').do(self.create_backup())

    def load(self):
        """Try to load an existing repository"""
        if path.exists(self._location):
            if path.isdir(self._location):
                self._creation_date = self.read_creation_date('creation_date')
                self._last_backup_date = self.read_creation_date('last_backup_date')
                self.create_repo_metadata_file(self._creation_date, self._last_backup_date)
                if self.is_backup_needed():
                    self._last_backup_date = datetime.utcnow().date()
                    self.create_repo_metadata_file(self._creation_date, self._last_backup_date)
                    self.create_backup(backup_file_name = self._name)

                self._name = read_ini_file(self._paths_file)['repository']['name']
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
        self._last_backup_date = datetime.strptime('0001/1/1', '%Y/%m/%d').date()
        self.create_repo_metadata_file(self._creation_date, self._last_backup_date)

    def absolute_path(self):
        if path.isabs(self._location):
            return self._location
        else:
            return path.abspath(self._location)

    def create_default_path_file(self):
        data = {
            'directories': FOLDERS_PATH,
            'files': {'repo_main_folder': path.basename(self._location),
                      'paths': self._paths_file,
                      'metadata': self._metadata_file},
            'repository': {'name': self._name}
        }
        write_ini_file(self._paths_file, data)

    def create_repo_metadata_file(self, date_obj, backup_date_obj):
        data = {
            'creation_date': {
                'year': date_obj.year,
                'month': date_obj.month,
                'day': date_obj.day,
                'hour': date_obj.hour,
                'minute': date_obj.minute,
                'second': date_obj.second,
                'microsecond': date_obj.microsecond
            },
            'last_backup_date': {
                'year': backup_date_obj.year,
                'month': backup_date_obj.month,
                'day': backup_date_obj.day}
        }
        write_ini_file(self._metadata_file, data)

    def read_creation_date(self, type_of_date):
        metadata_data = read_ini_file(self._metadata_file)
        if type_of_date == 'creation_date':
            return datetime.strptime('{} {} {} {} {} {} {}'.format(
                metadata_data[type_of_date]['year'],
                metadata_data[type_of_date]['month'],
                metadata_data[type_of_date]['day'],
                metadata_data[type_of_date]['hour'],
                metadata_data[type_of_date]['minute'],
                metadata_data[type_of_date]['second'],
                metadata_data[type_of_date]['microsecond']
            ), '%Y %m %d %H %M %S %f')
        elif type_of_date == 'last_backup_date':
            return datetime.strptime('{:0>4} {} {}'.format(
                metadata_data[type_of_date]['year'],
                metadata_data[type_of_date]['month'],
                metadata_data[type_of_date]['day']
            ), '%Y %m %d').date()

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
                        document_files_existence = self._document_manager.document_files_exist(document_id,
                                                                                               user_manager = self._user_manager)
                        for file_name_key, exists_value in document_files_existence.iteritems():
                            if not exists_value:
                                raise RuntimeError(
                                    "The {} file doesn't exists in the {} ID document!".format(file_name_key,
                                                                                               document_id))
                        document = self._document_manager.load_document(document_id, self._user_manager)
                        if not isinstance(document.author, list):
                            doc_author = [document.author]
                        else:
                            doc_author = document.author
                        if len(doc_author) == 0:
                            raise ValueError("No author related to document!")
                    except Exception as e:
                        rmtree(new_path)
                        raise e
            else:
                raise ValueError("No document to import from the '{}' path!".format(from_path))
        else:
            raise ValueError("The '{}' doesn't exists!".format(from_path))

    def export_documents(self, list_of_documents_id, path_to):
        if not path.exists(path_to):
            makedirs(path_to)
        for document_id in list_of_documents_id:
            document = self._document_manager.load_document(document_id)
            if document.state == 'accepted' and document.is_public():
                exported_document_path = path.join(self._document_manager._location, str(document_id))
                for file_name in listdir(exported_document_path):
                    if file_name != '{}_document_metadata.edd'.format(document_id):
                        copy2(path.join(exported_document_path, file_name), path_to)
                existing_metadata_file = '{}_document_metadata.edd'.format(document_id)
                remove(path.join(exported_document_path, existing_metadata_file))
                user = self._user_manager.find_user_by_id(document.author)
                data = {
                    'document': {
                        'title': document.title,
                        'description': document.description,
                        'author': '{} {}'.format(user.first_name, user.family_name),
                        'files': document.files,
                        'doc_format': document.doc_format,
                        'creation_date': document.creation_date,
                        'modification_date': document.modification_date
                    }}
                for key, value in data['document'].iteritems():
                    data['document'][key] = str(value)
                write_ini_file(path.join(path_to, '{}.edd'.format(document_id)), data)
            else:
                raise TypeError(
                    "The docuement must be accepted and public to export, "
                    "not {} and {}!".format(document.state, 'Private' if not document.is_public() else 'Public'))

    def create_backup(self, backup_file_name = 'backup', backup_path = './Backups', verbose = False,
                      date_format = '%Y/%m/%d %H:%M:%S', backup_documents = True, backup_logs = True,
                      backup_projects = True, backup_reports = True, backup_users = True):
        start_time = datetime.utcnow()
        if verbose:
            print("The backup of the {} repository has started on UTC {}.".format(self._name, start_time.strftime(
                date_format)))
        if not path.exists(backup_path):
            makedirs(backup_path)
            if verbose:
                print("The {} backup path structure is created.".format(backup_path))
        else:
            if verbose:
                print("The {} backup path exists.".format(backup_path))
        backup_file_name = self.determine_export_file_name(backup_file_name, backup_path)
        if verbose:
            print("The name of the backup file is: {}.zip.".format(backup_file_name))
        new_location = self._location
        if not (backup_documents and backup_logs and backup_projects and backup_reports and backup_users):
            pats_file = read_ini_file(self._paths_file)
            copytree(new_location, './{}'.format(backup_file_name))
            new_location = './{}'.format(backup_file_name)
            if not backup_documents:
                rmtree(path.join(self._location, pats_file['directories']['documents']))
                makedirs(path.join(self._location, pats_file['directories']['documents']))
            if not backup_logs:
                rmtree(path.join(self._location, pats_file['directories']['logs']))
                makedirs(path.join(self._location, pats_file['directories']['logs']))
            if not backup_projects:
                rmtree(path.join(self._location, pats_file['directories']['projects']))
                makedirs(path.join(self._location, pats_file['directories']['projects']))
            if not backup_reports:
                rmtree(path.join(self._location, pats_file['directories']['reports']))
                makedirs(path.join(self._location, pats_file['directories']['reports']))
            if not backup_users:
                rmtree(path.join(self._location, pats_file['directories']['users']))
                makedirs(path.join(self._location, pats_file['directories']['users']))
        make_archive(path.join(backup_path, backup_file_name), 'zip', new_location, verbose = verbose)  # logger =
        if new_location == './{}'.format(backup_file_name) and path.exists(new_location):
            rmtree(new_location)
        if verbose:
            end_time = datetime.utcnow()
            print("The backup is completed on UTC {}, please check the {} file".format(end_time.strftime(date_format),
                                                                                       path.join(backup_path,
                                                                                                 backup_file_name)))
            print("The process lasted {} seconds.".format((end_time - start_time).total_seconds()))

    def determine_export_file_name(self, backup_file_name, backup_path):
        if path.exists(path.join(backup_path, backup_file_name + '.zip')):
            new_backup_file_name = backup_file_name
            number = 1
            if '_' in backup_file_name:
                try:
                    number = int(backup_file_name.split('_')[-1])
                    new_backup_file_name = '_'.join(backup_file_name[:-1]) + '_{}'
                except ValueError:
                    new_backup_file_name += '_{}'
            else:
                new_backup_file_name += '_{}'

            while True:
                if new_backup_file_name.format(number) + '.zip' in listdir(backup_path):
                    number += 1
                else:
                    return new_backup_file_name.format(number)
        else:
            return backup_file_name

    def restore(self, backup_file_name = 'backup', backup_path = './Backups', verbose = False,
                date_format = '%Y/%m/%d %H:%M:%S', backup_documents = True, backup_logs = True,
                backup_projects = True, backup_reports = True, backup_users = True):
        start_time = datetime.utcnow()
        if verbose:
            print("The restore of the {} repository has started on UTC {}.".format(self._name, start_time.strftime(
                date_format)))
        rmtree(self._location)
        if verbose:
            print("The old repository is deleted on {} path.".format(self._location))

        with ZipFile(path.join(backup_path, backup_file_name + '.zip'), "r") as z:
            z.extractall(self._location)

        if not (backup_documents and backup_logs and backup_projects and backup_reports and backup_users):
            pats_file = read_ini_file(self._paths_file)
            unimported = []
            if not backup_documents:
                rmtree(path.join(self._location, pats_file['directories']['documents']))
                makedirs(path.join(self._location, pats_file['directories']['documents']))
                unimported.append('documents')
            if not backup_logs:
                rmtree(path.join(self._location, pats_file['directories']['logs']))
                makedirs(path.join(self._location, pats_file['directories']['logs']))
                unimported.append('logs')
            if not backup_projects:
                rmtree(path.join(self._location, pats_file['directories']['projects']))
                makedirs(path.join(self._location, pats_file['directories']['projects']))
                unimported.append('projects')
            if not backup_reports:
                rmtree(path.join(self._location, pats_file['directories']['reports']))
                makedirs(path.join(self._location, pats_file['directories']['reports']))
                unimported.append('reports')
            if not backup_users:
                rmtree(path.join(self._location, pats_file['directories']['users']))
                makedirs(path.join(self._location, pats_file['directories']['users']))
                unimported.append('users')
            if len(unimported) > 0:
                print("The {} were not imported.".format(', '.join(unimported)))

        if verbose:
            end_time = datetime.utcnow()
            print(
                "The restore is completed on UTC {}, please check the {} repository".format(
                    end_time.strftime(date_format),
                    self._location))
            print("The process lasted {} seconds.".format((end_time - start_time).total_seconds()))

    def show_repository_info(self, name = ''):
        paths = read_ini_file(self._paths_file)
        users = dict()
        documents = dict()
        roles = dict()

        for user_id in self._user_manager.find_all_users():
            users[user_id] = self._user_manager.load_user(user_id)
        for document_id in self._document_manager.find_all_documents():
            documents[document_id] = self._document_manager.load_document(document_id, self._user_manager)
        for role_key, user_ids_value in self._user_manager.list_users_by_role().iteritems():
            roles[role_key] = ', '.join([str(i) for i in user_ids_value])
        abs_path = path.dirname(path.abspath(__file__))

        env = Environment(loader = FileSystemLoader(path.join(abs_path, 'templates')))
        template = env.get_template('rep_info.html')
        output_from_parsed_template = template.render(repository_name = self._name, creation_date = self._creation_date,
                                                      backup_date = self._last_backup_date, paths = paths,
                                                      users = users, roles = roles, documents = documents)

        with open(path.join(abs_path, "index{}.html".format('_' + name)), "wb") as fh:
            fh.write(output_from_parsed_template)
        webbrowser.open(path.join(abs_path, "index{}.html".format('_' + name)))

    def show_backup_info(self, backup_file):
        if '.zip' not in backup_file:
            full_backup_file = backup_file + '.zip'
        else:
            full_backup_file = backup_file
        if path.exists(full_backup_file):
            abs_path = path.dirname(path.abspath(__file__))
            tmp_location = abs_path + '/tmp/tmp_repository'
            with ZipFile(full_backup_file, "r") as z:
                z.extractall(tmp_location)
            tmp_repo = Repository(location = tmp_location)
            tmp_repo.show_repository_info(name = path.basename(backup_file))
            rmtree(tmp_location)
        else:
            raise TypeError("The {} backup doesn't exists!".format(full_backup_file))

    def is_backup_needed(self):
        if (datetime.utcnow().date() - self._last_backup_date).days > BACKUP_FREQUENCY:
            return True
        else:
            return False
