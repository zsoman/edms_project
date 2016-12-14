import ConfigParser
from datetime import datetime
from os import path, makedirs
from shutil import move

from iniformat.reader import read_ini_file
from storage_utils import get_next_id

VALID_DOCUMENT_STATES = ['new', 'pending', 'accepted', 'rejected']
AFTER_NEW_STATE = ['pending']
AFTER_PENDING_STATE = ['accepted', 'rejected']


class Document(object):
    """Document of the repository"""

    def __init__(self, title, description, author, files, doc_format):
        self._title = title
        self._description = description
        self._author = author
        self._files = files
        self._doc_format = doc_format
        self._creation_date = datetime.utcnow()
        self._modification_date = self._creation_date
        self._state = 'new'
        self._is_public = False

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, value):
        self._files = value

    @property
    def creation_date(self):
        d = self._creation_date
        return '{}/{}/{} {}:{}:{} {}'.format(d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond)

    @property
    def modification_date(self):
        d = self._modification_date
        return '{}/{}/{} {}:{}:{} {}'.format(d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond)

    @modification_date.setter
    def modification_date(self, new_datetime):
        if isinstance(new_datetime, datetime):
            self._modification_date = new_datetime
        else:
            raise TypeError("The new date must be a datetime object and not {}!".format(type(new_datetime).__name__))

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value in VALID_DOCUMENT_STATES:
            self._state = value
        else:
            raise ValueError('The "{}" is an invalid document state!'.format(value))

    @property
    def doc_format(self):
        return self._doc_format

    @doc_format.setter
    def doc_format(self, value):
        self._doc_format = value

    def is_public(self):
        return self._is_public

    def make_public(self):
        self._is_public = True

    def make_private(self):
        self._is_public = False

    def change_state(self, new_state):
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


class DocumentManager(object):
    """Manage documents"""

    def __init__(self, repository):
        self._repository = repository
        metadata_data = read_ini_file(self._repository._paths_file)
        self._location = path.join(self._repository._location, metadata_data['directories']['documents'])

    def save_document(self, new_document_folder, new_document_id, document):
        basename_files_list = []
        for path_file in document.files:
            basename_files_list.append(path.basename(path_file))
            move(path_file, new_document_folder)
        data = {
            'title': document.title,
            'description': document.description,
            'author': document.author,
            'files': basename_files_list,
            'doc_format': document.doc_format,
            'creation_date': document.creation_date,
            'modification_date': document.modification_date,
            'state': document.state,
            'is_public': document.is_public()
        }
        parser = ConfigParser.ConfigParser()

        parser.add_section('document')
        for key in data.keys():
            parser.set('document', key, data[key])

        with open(path.join(new_document_folder, '{}_document_metadata.ini'.format(new_document_id)), 'w') as file_obj:
            parser.write(file_obj)


    def load_document(self):
        pass
        # TODO: loads a document by ID into an object, but it reads only the name of the file and not the path

    def add_document(self, document):
        new_document_id = get_next_id(self._location)
        new_document_folder = self.create_structure_for_document(new_document_id)
        self.save_document(new_document_folder, new_document_id, document)

    def create_structure_for_document(self, new_document_id):
        new_document_folder = path.join(self._location, str(new_document_id))
        makedirs(new_document_folder)
        return new_document_folder

    def update_document(self, document_id, document):
        pass
        # TODO: updates the document in the memory

    def remove_document(self, document_id):
        pass
        # TODO: remove document from the repository

    def all_available_doocuments(self):
        pass
        # TODO

    def find_document_by_id(self):
        pass
        # TODO

    def find_document_by_title(self):
        pass
        # TODO

    def find_document_by_author(self):
        pass
        # TODO

    def find_document_by_format(self):
        pass
        # TODO

    def document_files_exist(self):
        pass
        # TODO
