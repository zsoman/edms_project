#!/usr/bin/env python
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

# Imports -----------------------------------------------------------------------------------------------------------
import logging
import webbrowser
from datetime import datetime
from os import makedirs, path, utime, listdir, remove, environ
from shutil import copytree, rmtree, copy2, make_archive
from warnings import filterwarnings
from zipfile import ZipFile

import schedule
from jinja2 import Environment, FileSystemLoader

from documents import DocumentManager
from iniformat.reader import read_ini_file
from iniformat.writer import write_ini_file
from users import UserManager

# Authorship information  -------------------------------------------------------------------------------------------
__author__ = "Zsolt Bokor Levente"
__copyright__ = "Copyright 2016, Morgan Stanley - Training 360 Project"
__credits__ = __author__
__version__ = "1.0.0"
__maintainer__ = __author__
__email__ = ["bokor.zsolt5@gmail.com", "bokorzsolt@yahoo.com"]
__status__ = "Development"

# Setting up the logger # ________________________________________________________________________________________________________________ #
environ["NLS_LANG"] = ".AL32UTF8"
logger = logging.getLogger('repository')
logger.setLevel(logging.DEBUG)
filterwarnings("ignore")

# Parameters --------------------------------------------------------------------------------------------------------
ROLES_FILE = 'roles'
PATHS_FILE = 'paths.ini'
FOLDERS_PATH = {'documents': 'documents', 'logs': 'logs', 'projects': 'projects',
                'reports': 'reports', 'users': 'users'}
BACKUP_FREQUENCY = 7

# -------------------------------------------------------------------------------------------------------------------


class Repository(object):
    """Represents the document management system as a repository.

    The :py:class:Repository is defined by: name, location, metadata file's location, paths metadata file's location,
    roles file type, :py:class:UserManager object and :py:class:DocumentManagement object.
    """

    def __init__(self, name = 'Repository', location = path.join('Repositories', 'repo_1'), roles_file_type = 'txt'):
        """
        Initialisation of a new :py:class:Repository object.

        :param name: The name of the :py:class:Repository object, the default value is 'Repository'.
        :param location: The path of the :py:class:Repository object, the default value is 'Repositories/repo_1'.
        :param roles_file_type: The type of roles metadata file, it can be: TXT, XML, JSON.
        """
        self._name = name
        self._location = location
        self._metadata_file = path.join(self._location, '{}_metadata.edd'.format(path.basename(name)))
        self._paths_file = path.join(self._location, PATHS_FILE)
        if roles_file_type.lower() in ['txt', 'xml', 'json']:
            self._roles_file_type = roles_file_type.lower()
        else:
            raise ValueError("The roles_file_type must be txt, xml or json, not {}!".format(roles_file_type))
        self.load()
        self._user_manager = UserManager(self._location, self._paths_file)
        self._document_manager = DocumentManager(self._location, self._paths_file)
        schedule.every(BACKUP_FREQUENCY).days.at('4:00').do(self.create_backup)
        self.initialize_logger(self.location)
        logger.info("The repository is initialized.")

    @property
    def name(self):
        """
        The property of the :py:attr:_name attribute.

        :return: The name of the :py:class:Repository object :py:attr:_name.
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        The setter of the :py:attr:_name.

        :param value: New name.
        :return:
        """
        raise AttributeError("The repository object's name can't be changed!")

    @property
    def location(self):
        """
        The property of the :py:attr:_location attribute.

        :return: The location of the :py:class:Repository object :py:attr:_location`.
        """
        return self._location

    @location.setter
    def location(self, value):
        """
        The setter of the :py:attr:_location.

        :param value: New location.
        :return:
        """
        raise AttributeError("The repository object's location can't be changed!")

    @property
    def metadata_file(self):
        """
        The property of the :py:attr:_metadata_file attribute.

        :return: The metadata_file of the :py:class:Repository object :py:attr:_metadata_file.
        """
        return self._metadata_file

    @metadata_file.setter
    def metadata_file(self, value):
        """
        The setter of the :py:attr:_metadata_file.

        :param value: New metadata_file.
        :return:
        """
        raise AttributeError("The repository object's metadata_file location can't be changed!")

    @property
    def paths_file(self):
        """
        The property of the :py:attr:_paths_file attribute.

        :return: The paths_file of the :py:class:Repository object :py:attr:_paths_file.
        """
        return self._name

    @paths_file.setter
    def paths_file(self, value):
        """
        The setter of the :py:attr:_paths_file.

        :param value: New paths_file.
        :return:
        """
        raise AttributeError("The repository object's paths_file location can't be changed!")

    @property
    def roles_file_type(self):
        """
        The property of the :py:attr:_roles_file_type attribute.

        :return: The roles_file_type of the :py:class:Repository object :py:attr:_roles_file_type.
        """
        return self._roles_file_type

    @roles_file_type.setter
    def roles_file_type(self, value):
        """
        The setter of the :py:attr:_roles_file_type.

        :param value: New roles_file_type.
        :return:
        """
        raise AttributeError("The repository object's roles_file_type can't be changed!")

    @property
    def user_manager(self):
        """
        The property of the :py:attr:_user_manager attribute.

        :return: The user_manager of the :py:class:Repository object :py:attr:_user_manager.
        """
        return self._user_manager

    @user_manager.setter
    def user_manager(self, value):
        """
        The setter of the :py:attr:_user_manager.

        :param value: New user_manager.
        :return:
        """
        raise AttributeError("The repository object's user_manager object can't be changed!")

    @property
    def document_manager(self):
        """
        The property of the :py:attr:_document_manager attribute.

        :return: The document_manager of the :py:class:Repository object :py:attr:_document_manager.
        """
        return self._document_manager

    @document_manager.setter
    def document_manager(self, value):
        """
        The setter of the :py:attr:_document_manager.

        :param value: New document_manager.
        :return:
        """
        raise AttributeError("The repository object's document_manager object can't be changed!")


    def load(self):
        """
        Try to load a :py:class:Repository object. If the :py:attr:_location path already exists then it tries to load
        it, but if not it will create a new :py:class:Repository object by calling the :py:meth:initialize method.
        :exception ValueError is raised if the path is not a directory.
        :return:
        """
        if path.exists(self._location):
            if path.isdir(self._location):
                self._creation_date = self.read_date('creation_date')
                self._last_backup_date = self.read_date('last_backup_date')
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
        """
        Initialize a :py:class:Repository object on the :py:attr:_location path.
        :return:
        """
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
        """
        Determines the absolute path of the :py:class:Repository object.

        :return: The absolute path of the :py:class:Repository object.
        """
        if path.isabs(self._location):
            return self._location
        else:
            return path.abspath(self._location)

    def create_default_path_file(self):
        """
        Creates the paths file metadata file for the :py:class:Repository object and writes the data to file too.

        :return:
        """
        data = {
            'directories': FOLDERS_PATH,
            'files': {'repo_main_folder': path.basename(self._location),
                      'paths': self._paths_file,
                      'metadata': self._metadata_file},
            'repository': {'name': self._name}
        }
        write_ini_file(self._paths_file, data)
        logger.info("The path file is created and the data is written intto it.")

    def create_repo_metadata_file(self, date_obj, backup_date_obj):
        """
        Creates the :py:class:Repository object's metadata file and writes the data into it.

        :param date_obj: :py:attr:_cration_date attribute of the :py:class:Repository object.
        :param backup_date_obj: :py:attr:_last_backup_date attribute of the :py:class:Repository object.
        :return:
        """
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
        logger.info("The repository's metadata file is created and the data is written into it.")

    def read_date(self, type_of_date):
        """
        Reds the :py:attr:_creation_date or :py:attr:_last_backup_date attribute.

        :param type_of_date: 'creation_date' or 'last_backup_date'.
        :return: A datetime.datetime object or a datetime.date object in function of the ``type_of_date``.
        """
        metadata_data = read_ini_file(self._metadata_file)
        if type_of_date == 'creation_date':
            logger.info("The creation date is read form the repository's metadata file.")
            return datetime.strptime('{} {} {} {} {} {} {}'.format(
                metadata_data[type_of_date]['year'],
                metadata_data[type_of_date]['month'],
                metadata_data[type_of_date]['day'],
                metadata_data[type_of_date]['hour'],
                metadata_data[type_of_date]['minute'],
                metadata_data[type_of_date]['second'],
                metadata_data[type_of_date]['microsecond']), '%Y %m %d %H %M %S %f')
        elif type_of_date == 'last_backup_date':
            logger.info("The last backup date is read form the repository's metadata file.")
            return datetime.strptime('{:0>4} {} {}'.format(
                metadata_data[type_of_date]['year'],
                metadata_data[type_of_date]['month'],
                metadata_data[type_of_date]['day']), '%Y %m %d').date()

    @classmethod
    def find_all_documents_in_path(cls, from_path):
        """
        Finds all :py:class:Document objects in a path.

        :param from_path: The path where to search for :py:class:Document objects.
        :return: A list of available :py:class:Document IDs.
        """
        all_available_documents = []
        for file_or_folder in listdir(from_path):
            if path.isdir(path.join(from_path, file_or_folder)):
                try:
                    all_available_documents.append(int(file_or_folder))
                    logger.info("The {} directory is a repository document.".format(file_or_folder))
                except:
                    logger.debug("The {} file/directory is not a repository document.".format(file_or_folder))
        return all_available_documents

    def import_documents(self, from_path):
        """
        Imports all :py:class:Document objects from a path to the :py:class:Repository.

        :param from_path: The path where to search for :py:class:Document objects.
        :exception RuntimeError is raised if the :py:class:Document object doesn't contains the referenced file.
        :exception ValueError is raised if the :py:class:Document object has no author.
        :exception ValueError is raised if there is no available :py:class:Document objects on the ``from_path`` path.
        :exception ValueError is raised if the ``from_path`` doesn't exists.
        :return:
        """
        if path.exists(from_path):
            all_documents = Repository.find_all_documents_in_path(from_path)
            logger.debug("All documents are loaded form the {} path.".format(from_path))
            metadata_data = read_ini_file(self._paths_file)
            logger.debug("The content repositories metadata file is loaded.")
            to_path = path.join(self._location, metadata_data['directories']['documents'])
            if len(all_documents) > 0:
                for document_id in all_documents:
                    new_path = reduce(path.join, [to_path, str(document_id)])
                    old_path = path.join(from_path, str(document_id))
                    copytree(old_path, new_path)
                    logger.info("The {} directory's content is copied to {} path.".format(old_path, new_path))
                    try:
                        document_files_existence = self._document_manager.document_files_exist(document_id,
                                                                                               user_manager = self._user_manager)
                        for file_name_key, exists_value in document_files_existence.iteritems():
                            if not exists_value:
                                logger.exception("The {} file doesn't exists in the {} ID document!".format(
                                    file_name_key, document_id))
                                raise RuntimeError("The {} file doesn't exists in the {} ID document!".format(
                                    file_name_key, document_id))
                        logger.info("All the directory's files exist.")
                        document = self._document_manager.load_document(document_id, self._user_manager)
                        logger.debug("The document with {} ID is loaded into the memory".format(document_id))
                        if not isinstance(document.author, list):
                            doc_author = [document.author]
                        else:
                            doc_author = document.author
                        if len(doc_author) == 0:
                            logger.exception("No author related to document!")
                            raise ValueError("No author related to document!")
                    except Exception as e:
                        rmtree(new_path)
                        logger.exception("An {} exception is raised when importing the document with {} ID.".format(
                            e.__class__.__name__, document_id))
                        raise e
            else:
                logger.exception("No document to import from the '{}' path!".format(from_path))
                raise ValueError("No document to import from the '{}' path!".format(from_path))
        else:
            logger.exception("The '{}' doesn't exists!".format(from_path))
            raise ValueError("The '{}' doesn't exists!".format(from_path))

    def export_documents(self, list_of_documents_id, path_to):
        """
        Exports all :py:class:Document objects in the ``list_of_documents_id`` from the :py:class:Repository object
        to the ``path_to`` path.

        :param list_of_documents_id: List of :py:class:Document object IDs to export.
        :param path_to: The path to export the :py:class:Document objects.
        :exception TypeError is raised if a not accepted and private :py:class:Document object is exported.
        :return:
        """
        if not path.exists(path_to):
            makedirs(path_to)
            logger.info("The {} path is created.".format(path_to))
        for document_id in list_of_documents_id:
            document = self._document_manager.load_document(document_id)
            logger.debug("The document with {} ID is loaded into the memory.".format(document_id))
            if document.state == 'accepted' and document.is_public():
                logger.debug("The document with {} id is in accepted state and is public.".format(document_id))
                exported_document_path = path.join(self._document_manager._location, str(document_id))
                for file_name in listdir(exported_document_path):
                    if file_name != '{}_document_metadata.edd'.format(document_id):
                        copy2(path.join(exported_document_path, file_name), path_to)
                        logger.info("The {} ID document's {} file is copied to {}.".format(
                            document_id, path.join(exported_document_path, file_name), path_to))
                existing_metadata_file = '{}_document_metadata.edd'.format(document_id)
                remove(path.join(exported_document_path, existing_metadata_file))
                logger.debug("The {} metadata file is deleted.".format(
                    path.join(exported_document_path, existing_metadata_file)))
                user = self._user_manager.find_user_by_id(document.author)
                logger.debug("The {} ID user (author of the document) is loaded.".format(document.author))
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
                logger.info("The document's metadata file is written to the filesystem.")
            else:
                logger.exception("The docuement must be accepted and public to export, not {} and {}!".format(
                        document.state, 'Private' if not document.is_public() else 'Public'))
                raise TypeError("The docuement must be accepted and public to export, not {} and {}!".format(
                        document.state, 'Private' if not document.is_public() else 'Public'))

    def create_backup(self, backup_file_name = 'backup', backup_path = './Backups', verbose = False,
                      date_format = '%Y/%m/%d %H:%M:%S', backup_documents = True, backup_logs = True,
                      backup_projects = True, backup_reports = True, backup_users = True):
        """
        Creates a backup of the :py:class:Repository object to the ``backup_path`` with ``backup_file_name``.

        :param backup_file_name: The backup files name of the :py:class:Repository object, the default value is 'backup'.
        :param backup_path: The backup path where the ``backup_file_name`` is saved, the default value is './Backups'
        :param verbose: Bool, if it's True it will print out some information about the backup process, default value
        is False.
        :param date_format: The date format in which the date are printed out if the ``verbose`` parameter is True,
        the default value is '%Y/%m/%d %H:%M:%S'.
        :param backup_documents: Bool, determines if to back up the :py:class:Document objects of the
        :py:class:Repository.
        :param backup_logs: Bool, determines if to back up the log files of the :py:class:Repository.
        :param backup_projects: Bool, determines if to back up the :py:class:Project objects of the
        :py:class:Repository.
        :param backup_reports: Bool, determines if to back up the :py:class:Report objects of the
        :py:class:Repository.
        :param backup_users: Bool, determines if to back up the :py:class:User objects of the
        :py:class:Repository.
        :return:
        """
        start_time = datetime.utcnow()
        logger.info("The backup of the {} repository has started on UTC {}.".format(self._name, start_time.strftime(
            date_format)))
        if verbose:
            print("The backup of the {} repository has started on UTC {}.".format(self._name, start_time.strftime(
                date_format)))
        if not path.exists(backup_path):
            makedirs(backup_path)
            logger.info("The {} backup path structure is created.".format(backup_path))
            if verbose:
                print("The {} backup path structure is created.".format(backup_path))
        else:
            logger.info("The {} backup path exists.".format(backup_path))
            if verbose:
                print("The {} backup path exists.".format(backup_path))
        backup_file_name = self.determine_export_file_name(backup_file_name, backup_path)
        logger.info("The name of the backup file is: {}.zip.".format(backup_file_name))
        if verbose:
            print("The name of the backup file is: {}.zip.".format(backup_file_name))
        new_location = self._location
        if not (backup_documents and backup_logs and backup_projects and backup_reports and backup_users):
            pats_file = read_ini_file(self._paths_file)
            copytree(new_location, './{}'.format(backup_file_name))
            logger.debug("The backup file is copied from to {} with {} name.".format(new_location,
                                                                                     './{}'.format(backup_file_name)))
            new_location = './{}'.format(backup_file_name)
            if not backup_documents:
                rmtree(path.join(self._location, pats_file['directories']['documents']))
                makedirs(path.join(self._location, pats_file['directories']['documents']))
                logger.debug("The {} directory is removed.".format(
                    path.join(self._location, pats_file['directories']['documents'])))
            if not backup_logs:
                rmtree(path.join(self._location, pats_file['directories']['logs']))
                makedirs(path.join(self._location, pats_file['directories']['logs']))
                logger.debug(
                    "The {} directory is removed.".format(path.join(self._location, pats_file['directories']['logs'])))
            if not backup_projects:
                rmtree(path.join(self._location, pats_file['directories']['projects']))
                makedirs(path.join(self._location, pats_file['directories']['projects']))
                logger.debug("The {} directory is removed.".format(
                    path.join(self._location, pats_file['directories']['projects'])))
            if not backup_reports:
                rmtree(path.join(self._location, pats_file['directories']['reports']))
                makedirs(path.join(self._location, pats_file['directories']['reports']))
                logger.debug("The {} directory is removed.".format(
                    path.join(self._location, pats_file['directories']['reports'])))
            if not backup_users:
                rmtree(path.join(self._location, pats_file['directories']['users']))
                makedirs(path.join(self._location, pats_file['directories']['users']))
                logger.debug(
                    "The {} directory is removed.".format(path.join(self._location, pats_file['directories']['users'])))
        make_archive(path.join(backup_path, backup_file_name), 'zip', new_location, verbose = verbose)  # logger =
        if new_location == './{}'.format(backup_file_name) and path.exists(new_location):
            rmtree(new_location)
        if verbose:
            end_time = datetime.utcnow()
            print("The backup is completed on UTC {}, please check the {} file".format(
                end_time.strftime(date_format), path.join(backup_path, backup_file_name)))
            print("The process lasted {} seconds.".format((end_time - start_time).total_seconds()))
            logger.info("The backup is completed on UTC {}, please check the {} file".format(
                end_time.strftime(date_format), path.join(backup_path, backup_file_name)))
            logger.info("The process lasted {} seconds.".format((end_time - start_time).total_seconds()))

    def determine_export_file_name(self, backup_file_name, backup_path):
        """
        Determines based on the :py:meth:create_backup methods ``backup_file_name`` parameter the backup files name.

        :param backup_file_name: The :py:meth:create_backup methods ``backup_file_name``.
        :param backup_path: :py:meth:create_backup methods ``backup_path``.
        :return: The new backup files name.
        """
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
        """
        Restores a :py:class:Repository object from the filesystem and deletes the old :py:class:Repository object.

        :param backup_file_name: The backup files name of the :py:class:Repository object, the default value is 'backup'.
        :param backup_path: The backup path from where the ``backup_file_name`` will be restored, the default value
        is './Backups'
        :param verbose: Bool, if it's True it will print out some information about the restore process, default value
        is False.
        :param date_format: The date format in which the date are printed out if the ``verbose`` parameter is True,
        the default value is '%Y/%m/%d %H:%M:%S'.
        :param backup_documents: Bool, determines if to restore the :py:class:Document objects of the
        :py:class:Repository.
        :param backup_logs: Bool, determines if to restpre the log files of the :py:class:Repository.
        :param backup_projects: Bool, determines if to restore the :py:class:Project objects of the
        :py:class:Repository.
        :param backup_reports: Bool, determines if to restore the :py:class:Report objects of the :py:class:Repository.
        :param backup_users: Bool, determines if to restore the :py:class:User objects of the :py:class:Repository.
        """
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
                    end_time.strftime(date_format), self._location))
            print("The process lasted {} seconds.".format((end_time - start_time).total_seconds()))

    def show_repository_info(self, name = ''):
        """
        Shows some information about the :py:class:Repository object in an index.html file.

        The following information is getherd in the HTML file: :py:class:Repository object :py:attr:name,
        :py:attr:_creation_date, :py:attr:_last_backup_date, the :py:attr:path_file meta data, number and all
        :py:class:User objects, all :py:class:Roles object and the number and all :py:class:Document objects.

        :param name: This attribute is not used to show information about an actual :py:class:Repository, because the
        information is printed into the index.html file, but we can prin out information about an archived
        :py:class:Repository too, and for those this parameter is the name of the backup file.
        :return:
        """
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
        """
        It will print into an HTML file the information of a backed up :py:class:Repository object with the help of the
        :py:meth:show_repository_info method.

        The HTML file will be like: index_[name_of_the_backup_file].HTML.

        :param backup_file: The backed up :py:class:Repository file, path and file name.
        :return:
        """
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
        """
        This metod is called every time a :py:class:Repository object is loaded with the :py:meth:load method. If the
        :py:attr:_last_backup_date is older than the :py:const:BACKUP_FREQUENCY in days.

        :return: Bool.
        """
        if (datetime.utcnow().date() - self._last_backup_date).days > BACKUP_FREQUENCY:
            return True
        else:
            return False

    def initialize_logger(self, repository_path):
        debug_file_logger = logging.FileHandler(reduce(path.join, [repository_path, 'logs', 'debug_log.log']))
        debug_file_logger.setLevel(logging.DEBUG)
        info_file_logger = logging.FileHandler(reduce(path.join, [repository_path, 'logs', '_log.log']))
        info_file_logger.setLevel(logging.INFO)
        console_logger = logging.StreamHandler()
        console_logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(processName)s / %(threadName)s - %(name)s - %(levelname)s - %(message)s')
        debug_file_logger.setFormatter(formatter)
        info_file_logger.setFormatter(formatter)
        console_logger.setFormatter(formatter)

        logger.addHandler(debug_file_logger)
        logger.addHandler(info_file_logger)
        logger.addHandler(console_logger)
