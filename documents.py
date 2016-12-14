from datetime import datetime
from os import path

from iniformat.reader import read_ini_file


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
    def state(self):
        return self._state


    @state.setter
    def state(self, value):
        if value in ['new', 'pending', 'accepted', 'rejected']:
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
        pass
        # TODO: needs to check if it is a valid state and if the state is reachable


class DocumentManager(object):
    """Manage documents"""


    def __init__(self, repository):
        self._repository = repository
        metadata_data = read_ini_file(self._repository._paths_file)
        self._location = path.join(self._repository._location,
                                   metadata_data['directories']['documents'])


    def save_document(self):
        pass
        # TODO: save the document object to the repository, and copy the original file to the repository


    def load_document(self):
        pass
        # TODO: loads a document by ID into an object, but it reads only the name of the file and not the path


    def add_document(self, document):
        pass
        # TODO: add document to the repository


    def create_structure_for_document(self):
        pass
        # TODO: it creates the folder structure and the metadata


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
