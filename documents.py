#!/usr/bin/env python
"""This file contains the implementation of Documents and DocumentManager classes.

The documents are represented as a directory which name is a number, ID. This directory includes the files that are
represented in the document's abstraction level. The document manager operates on documents: count, save, add, load etc.
"""

# Imports -----------------------------------------------------------------------------------------------------------
from datetime import datetime
from os import path, makedirs, listdir, remove
from shutil import move, rmtree

from iniformat.reader import read_ini_file
from iniformat.writer import write_ini_file
from storage_utils import get_next_id

VALID_DOCUMENT_STATES = ['new', 'pending', 'accepted', 'rejected']
AFTER_NEW_STATE = ['pending']
AFTER_PENDING_STATE = ['accepted', 'rejected']

# Authorship information  -------------------------------------------------------------------------------------------
__author__ = "Zsolt Bokor Levente"
__copyright__ = "Copyright 2016, Morgan Stanely - Training 360 Project"
__credits__ = "Zsolt Bokor Levente"
__version__ = "1.0.0"
__maintainer__ = "Zsolt Bokor Levente"
__email__ = ["bokor.zsolt5@gmail.com", "bokorzsolt@yahoo.com"]
__status__ = "Development"


# -------------------------------------------------------------------------------------------------------------------

class DocumentDoesntExistsError(Exception):
    """This exception is raised when a document doesn't exists.
    """
    pass


class Document(object):
    """Document of the repository.

    The document is represented by: title, description, author(s): list of user IDs, files: list of files represented in
    the filesystem, document format: the format of the documents, creation date, modification date, state: new, pending,
    accepted, rejected; public/private.
    """

    def __init__(self, title, description, author, files, doc_format):
        """
        Initialisation of a new Document object.

        :param title: New title of the document.
        :param description: New description of the document.
        :param author: New author(s) of the document.
        :param files: New file(s) of the document.
        :param doc_format: New document format of the document.
        """
        self._title = title
        self._description = description
        if isinstance(author, list):
            self._author = author
        else:
            self._author = [author]
        self._files = files
        self._doc_format = doc_format
        self._creation_date = datetime.utcnow()
        self._modification_date = self._creation_date
        self._state = 'new'
        self._is_public = False

    @property
    def title(self):
        """
        The property of the :py:attr:_title attribute.

        :return: The title of the Document object :py:attr:_title.
        """
        return self._title

    @title.setter
    def title(self, value):
        """
        The setter of the :py:attr:_title.

        :param value: New title.
        :return:
        """
        self._title = value

    @property
    def description(self):
        """
        The property of the :py:attr:_description attribute.

        :return: The description of the Document object :py:attr:_description.
        """
        return self._description

    @description.setter
    def description(self, value):
        """
        The setter of the :py:attr:_description.

        :param value: New description.
        :return:
        """
        self._description = value

    @property
    def author(self):
        """
        The property of the :py:attr:_author attribute.

        :return: The author(s) of the Document object :py:attr:_author.
        """
        if len(self._author) == 1:
            return int(self._author[0])
        else:
            return self._author

    @author.setter
    def author(self, value):
        """
        The setter of the :py:attr:_author.

        :param value: New author(s).
        :return:
        """
        self._author = value

    @property
    def files(self):
        """
        The property of the :py:attr:_files attribute.

        :return: The file(s) of the Document object :py:attr:_files.
        """
        return self._files

    @files.setter
    def files(self, value):
        """
        The setter of the :py:attr:_files.

        :param value: New file(s).
        :return:
        """
        self._files = value

    @property
    def creation_date(self):
        """
        The property of the :py:attr:_creation_date attribute.

        :return: String representation of a date in the following format: YEAR/MONTH/DAY HOUR:MINUTES:SECONDS
        MILLISECONDS. The creation date of the Document object :py:attr:_creation_date.
        """
        d = self._creation_date
        return '{}/{}/{} {}:{}:{} {}'.format(d.year, d.month, d.day, d.hour, d.minute,
                                             d.second, d.microsecond)

    @creation_date.setter
    def creation_date(self, new_datetime):
        """
        The setter of the :py:attr:_creation_date.

        :param new_datetime: New date object. This parameter must be a :py:mod:datetime object, else a :py:exc:TypeError
        is raised.
        :exception TypeError is raised if the ``new_datetime`` parameter is not a :py:mod:datetime object.
        :return:
        """
        if isinstance(new_datetime, datetime):
            self._creation_date = new_datetime
        else:
            raise TypeError("The new date must be a datetime object and not {}!".format(
                type(new_datetime).__name__))

    @property
    def modification_date(self):
        """
        The property of the :py:attr:_modification_date attribute.

        :return: String representation of a date in the following format: YEAR/MONTH/DAY HOUR:MINUTES:SECONDS
        MILLISECONDS. The modification date of the Document object :py:attr:_modification_date.
        """
        d = self._modification_date
        return '{}/{}/{} {}:{}:{} {}'.format(d.year, d.month, d.day, d.hour, d.minute,
                                             d.second, d.microsecond)

    @modification_date.setter
    def modification_date(self, new_datetime):
        """
        The setter of the :py:attr:_modification_date.

        :param new_datetime: New date object. This parameter must be a :py:mod:datetime object, else a :py:exc:TypeError
        is raised.
        :exception TypeError is raised if the ``new_datetime`` parameter is not a :py:mod:datetime object.
        :return:
        """
        if isinstance(new_datetime, datetime):
            self._modification_date = new_datetime
        else:
            raise TypeError("The new date must be a datetime object and not {}!".format(
                type(new_datetime).__name__))

    @property
    def state(self):
        """
        The property of the :py:attr:_state attribute.

        :return: The state of the Document object :py:attr:_state.
        """
        return self._state

    @state.setter
    def state(self, value):
        """
        The setter of the :py:attr:_state.

        :param value: New state. If the ``value`` parameter is not a valid state (new, pending, accepted, rejected) a
        :py:exc:ValueError is raised.
        :exception ValueError is raised if the ``value`` parameter is not in :py:const:VALID_DOCUMENT_STATES list of
        valid states.
        :return:
        """
        if value in VALID_DOCUMENT_STATES:
            self._state = value
        else:
            raise ValueError('The "{}" is an invalid document state!'.format(value))

    @property
    def doc_format(self):
        """
        The property of the :py:attr:_doc_format attribute.

        :return: The document format of the Document object :py:attr:_doc_format.
        """
        return self._doc_format

    @doc_format.setter
    def doc_format(self, value):
        """
        The setter of the :py:attr:_doc_format.

        :param value: New document format.
        :return:
        """
        self._doc_format = value

    def is_public(self):
        """
        Returns the visibility of the document.

        :return: If the :py:attr:is_public attribute is True it returns True, if it's False it returns false.
        """
        return self._is_public

    def make_public(self):
        """
        Makes the document public. Sets the :py:attr:is_public attribute to True.

        :return:
        """
        self._is_public = True

    def make_private(self):
        """
        Makes the document private. Sets the :py:attr:is_public attribute to False.

        :return:
        """
        self._is_public = False

    def change_state(self, new_state):
        """
        Changes the state of the document from it's actual :py:attr:state to ``new_state`` if it's a reachable state.

        :param new_state: The state to change the :py:attr:state to.
        :return:
        """
        if new_state not in VALID_DOCUMENT_STATES:
            raise ValueError("The {} state is not a valid state!".format(new_state))
        else:
            if self.state == 'new' and new_state in AFTER_NEW_STATE:
                self.state = new_state
            elif self.state == 'pending' and new_state in AFTER_PENDING_STATE:
                self.state = new_state
            else:
                if self.state == 'new':
                    raise ValueError(
                        "Because the current state is 'new' the new state must be "
                        "{}, can't be {}!".format(', '.join(AFTER_NEW_STATE),
                                                  new_state))
                elif self.state == 'pending':
                    raise ValueError(
                        "Because the current state is 'pending' the new state must "
                        "be {}, can't be {}!".format(', '.join(AFTER_PENDING_STATE),
                                                     new_state))

    def __str__(self):
        """
        String representation of the :py:class:Document.

        :return: Document represented by a string in the following format: :py:attr:title - :py:attr:author :
        :py:attr:description ; :py:attr:files ; :py:attr:doc_format.
        """
        document_string = ''
        document_string += self.title + ' - '
        document_string += str(self.author) + ': '
        document_string += self.description + '; '
        document_string += str(self.files) + '; '
        document_string += self.doc_format
        return document_string


class DocumentManager(object):
    """Manage documents in a repository.

    :py:class:DocumentManager contains the methods to manage the documents in a repository. For example: save a document,
    load, add documents to reposritory, update, remove, create backup and load backup etc.
    """

    def __init__(self, repository_location, paths_file = None):
        """
        Initialisation of a new DocumentManager object.

        :param repository_location: The path of the repository for which is working.
        :param paths_file: The path where the repositorie's paths_file is, this is a metadata file of the repository.
        """
        if not paths_file:
            self._location = repository_location
        else:
            metadata_data = read_ini_file(paths_file)
            self._location = path.join(repository_location, metadata_data['directories']['documents'])

    def save_document(self, new_document_folder, new_document_id, document):
        """
        This method saves a :py:class:Repository object to the filesystem.

        Moves the files stored in the :py:attr:files attribute of the document to the document's path and writes the
        metadata file [ID]_document_metadata.edd in the document directory. This file stores all the attributes of the
        :py:class:Document class.
        :param new_document_folder: The path of the document, the name of the document is a number, ID.
        :param new_document_id: The ID of the new document.
        :param document: :py:class:Document object to save to the filesystem.
        :return:
        """
        basename_files_list = []
        for path_file in document.files:
            basename_files_list.append(path.basename(path_file))
            move(path_file, new_document_folder)
        data = {
            'document': {
                'title': document.title,
                'description': document.description,
                'author': document.author,
                'files': basename_files_list,
                'doc_format': document.doc_format,
                'creation_date': document.creation_date,
                'modification_date': document.modification_date,
                'state': document.state,
                'is_public': document.is_public()
            }}

        for key, value in data['document'].iteritems():
            data['document'][key] = str(value)

        write_ini_file(path.join(new_document_folder, '{}_document_metadata.edd'.format(new_document_id)), data)

    def load_document(self, document_id, user_manager = None):
        """
        Loads a document to the memory.

        :param document_id: The ID of the :py:class:Document.
        :param user_manager: The user manager object of the :py:UserManager class.
        :exception DocumentDoesntExistsError is raised when the document is missing from the filesystem,
        :return: :py:class:Document object.
        """
        document_path = path.join(self._location, str(document_id))
        if not path.exists(document_path):
            raise DocumentDoesntExistsError("The {} path doesn't exists, so the document with {} id can't be loaded"
                                            "!".format(document_path, document_id))
        else:
            metadata_file = reduce(path.join,
                                   [self._location, str(document_id), '{}_document_metadata.edd'.format(document_id)])
            meta_data = read_ini_file(metadata_file)
            list_of_files = (
                [str(file_name.strip("'")) for file_name in meta_data['document']['files'][1:-1].split(', ')])
            if 'author' in meta_data['document']:
                if '[' in meta_data['document']['author'] and ']' in meta_data['document']['author']:
                    list_of_authors = [int(file_name.strip("'")) for file_name in
                                       meta_data['document']['author'][1:-1].split(', ')]
                else:
                    list_of_authors = meta_data['document']['author']
            else:
                if '[' in meta_data['document']['author_name'] and ']' in meta_data['document']['author_name']:
                    list_of_authors_by_name = [file_name.strip("'") for file_name in
                                               meta_data['document']['author_name'][1:-1].split(', ')]
                else:
                    list_of_authors_by_name = meta_data['document']['author_name']
                if not isinstance(list_of_authors_by_name, list):
                    list_of_authors_by_name = [list_of_authors_by_name]
                list_of_authors = set()
                for author_name in list_of_authors_by_name:
                    for user_id in user_manager.find_users_by_name(author_name):
                        list_of_authors.add(int(user_id))
                list_of_authors = list(list_of_authors)
            document = Document(meta_data['document']['title'], meta_data['document']['description'], list_of_authors,
                                list_of_files, meta_data['document']['doc_format'])
            document.creation_date = datetime.strptime(meta_data['document']['creation_date'], '%Y/%m/%d %H:%M:%S %f')
            document.modification_date = datetime.strptime(meta_data['document']['modification_date'],
                                                           '%Y/%m/%d %H:%M:%S %f')
            if 'author' in meta_data['document']:
                document.state = meta_data['document']['state']
                if meta_data['document']['is_public'] == 'True':
                    document.make_public()
            else:
                document.state = 'new'
                document.make_private()
            return document

    def add_document(self, document, new_document_folder = None):
        """
        This method adds a :py:class:Document object to the :py:class:ClassRepository. In addition to do this the
        :py:func:save_document function is calls to save a document to the filesystem.

        :return: :py:class:Document object.
        :param new_document_folder: :py:class:Document object.
        :return: The ID of the new document.
        """
        new_document_id = get_next_id(self._location)
        if not new_document_folder:
            new_document_folder = self.create_structure_for_document(new_document_id)
        self.save_document(new_document_folder, new_document_id, document)
        return new_document_id

    def create_structure_for_document(self, new_document_id):
        """
        Creates the directories necessary directories.

        :param new_document_id: The ID of a new :py:class:Document.
        :return: The path of the new document directory.
        """
        new_document_folder = path.join(self._location, str(new_document_id))
        makedirs(new_document_folder)
        return new_document_folder

    def update_document(self, document_id, document):
        """
        Updates a :py:class:Document object, searches for the directory by ID

        :param document_id: The ID of :py:class:Document object to update.
        :param document: New :py:class:Document object which contains the data to update the old :py:class:Document.
        :exception ValueError is raised if no document is found by the ``document_id``.
        :return:
        """
        if document_id not in self.find_all_documents():
            raise ValueError("The document with {} can't be updated because doesn't exists!".format(document_id))
        else:
            document_path = path.join(self._location, str(document_id))
            self.save_document(document_path, document_id, document)

    def remove_document(self, document_id):
        document_path = path.join(self._location, str(document_id))
        if path.exists(document_path):
            rmtree(document_path)
        else:
            raise ValueError("The document with the {} ID doesn't exists, it can't be removed!".format(document_id))

    def find_all_documents(self):
        all_available_documents = []
        for file_or_folder in listdir(self._location):
            if path.isdir(path.join(self._location, file_or_folder)):
                try:
                    all_available_documents.append(int(file_or_folder))
                except:
                    pass
        return all_available_documents

    def count_documents(self):
        return len(self.find_all_documents())

    def load_all_documents(self, user_manager = None):
        all_documents = dict()
        for document_id in self.find_all_documents():
            all_documents[document_id] = self.load_document(document_id, user_manager = user_manager)
        return all_documents

    def find_document_by_id(self, document_id, user_manager = None):
        if document_id not in self.find_all_documents():
            raise ValueError(
                "The document with {} ID doesn't exists, it can't be loaded!".format(document_id))
        else:
            return self.load_all_documents(user_manager = user_manager)[document_id]

    def find_documents_by_title(self, title):
        documents_by_title = dict()
        for doc_id_key, doc_value in self.load_all_documents().iteritems():
            if doc_value.title.lower() == title.lower():
                documents_by_title[doc_id_key] = doc_value
        if len(documents_by_title) == 0:
            raise DocumentDoesntExistsError("No document was found with {} title!".format(title))
        else:
            return documents_by_title.values()

    def find_documents_by_author(self, author, user_manager = None):
        documents_by_author = dict()
        for doc_id_key, doc_value in self.load_all_documents(user_manager = user_manager).iteritems():
            if isinstance(doc_value.author, list):
                authors = doc_value.author
            else:
                authors = [doc_value.author]
            if author in authors:
                documents_by_author[doc_id_key] = doc_value
        if len(documents_by_author) == 0:
            raise DocumentDoesntExistsError("No document was found with {} author!".format(author))
        else:
            return documents_by_author.values()

    def find_documents_by_format(self, format):
        documents_by_author = dict()
        for doc_id_key, doc_value in self.load_all_documents().iteritems():
            if format == doc_value.doc_format:
                documents_by_author[doc_id_key] = doc_value
        if len(documents_by_author) == 0:
            raise DocumentDoesntExistsError("No document was found with {} format!".format(format))
        else:
            return documents_by_author.values()

    def document_files_exist(self, document_id, user_manager = None):
        existence_of_document_files = dict()
        if document_id not in self.find_all_documents():
            raise ValueError("The docuement with {} ID doesn't exists!".format(document_id))
        else:
            document_path = path.join(self._location, str(document_id))
            document = self.find_document_by_id(document_id, user_manager = user_manager)
            for document_file in document.files:
                document_file_path = path.join(document_path, document_file)
                if path.exists(document_file_path) and path.isfile(document_file_path):
                    existence_of_document_files[document_file] = True
                else:
                    existence_of_document_files[document_file] = False
        if len(existence_of_document_files) == 0:
            raise RuntimeError("The document with {} ID doesn't contains registered files!".format(document_id))
        return existence_of_document_files

    def unreferenced_document_files(self, document_id):
        unreferenced_document_files = dict()
        if document_id not in self.find_all_documents():
            raise DocumentDoesntExistsError("The docuement with {} ID doesn't exists!".format(document_id))
        else:
            document_path = path.join(self._location, str(document_id))
            document = self.find_document_by_id(document_id)
            for document_file in listdir(document_path):
                if document_file != '{}_document_metadata.edd'.format(
                        document_id) and document_file not in document.files:
                    unreferenced_document_files[document_file] = False
                else:
                    unreferenced_document_files[document_file] = True
        if len(unreferenced_document_files) == 0:
            raise RuntimeError("The document with {} ID doesn't contains registered files!".format(document_id))
        return unreferenced_document_files

    def remove_document_files(self, document_id):
        if document_id not in self.find_all_documents():
            raise DocumentDoesntExistsError("The docuement with {} ID doesn't exists!".format(document_id))
        else:
            document_path = path.join(self._location, str(document_id))
            for file_name_key, exist_value in self.unreferenced_document_files(document_id).iteritems():
                if not exist_value:
                    document_file_path = path.join(document_path, file_name_key)
                    remove(document_file_path)
