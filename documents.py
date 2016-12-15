from datetime import datetime
from os import path, makedirs, listdir, remove
from shutil import move, rmtree

from iniformat.reader import read_ini_file
from iniformat.writer import write_ini_file
from repository import Repository
from storage_utils import get_next_id

VALID_DOCUMENT_STATES = ['new', 'pending', 'accepted', 'rejected']
AFTER_NEW_STATE = ['pending']
AFTER_PENDING_STATE = ['accepted', 'rejected']


class DocumentDoesntExistsError(Exception):
    pass


class Document(object):
    """Document of the repository"""


    def __init__(self, title, description, author, files, doc_format):
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
        if len(self._author) == 1:
            return int(self._author[0])
        else:
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
        return '{}/{}/{} {}:{}:{} {}'.format(d.year, d.month, d.day, d.hour, d.minute,
                                             d.second, d.microsecond)


    @creation_date.setter
    def creation_date(self, new_creation_date):
        self._creation_date = new_creation_date


    @property
    def modification_date(self):
        d = self._modification_date
        return '{}/{}/{} {}:{}:{} {}'.format(d.year, d.month, d.day, d.hour, d.minute,
                                             d.second, d.microsecond)


    @modification_date.setter
    def modification_date(self, new_modification_date):
        self._modification_date = new_modification_date


    @modification_date.setter
    def modification_date(self, new_datetime):
        if isinstance(new_datetime, datetime):
            self._modification_date = new_datetime
        else:
            raise TypeError("The new date must be a datetime object and not {}!".format(
                    type(new_datetime).__name__))


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


    def __str__(self):
        document_string = ''
        document_string += self.title + ' - '
        document_string += str(self.author) + ': '
        document_string += self.description + '; '
        document_string += str(self.files) + '; '
        document_string += self.doc_format
        return document_string


class DocumentManager(object):
    """Manage documents"""


    def __init__(self, repository):
        if isinstance(repository, Repository):
            self._repository = repository
        else:
            self._repository = Repository(location=repository)
        metadata_data = read_ini_file(self._repository._paths_file)
        self._location = path.join(self._repository._location, metadata_data['directories']['documents'])


    def save_document(self, new_document_folder, new_document_id, document):
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


    def load_document(self, document_id):
        document_path = path.join(self._location, str(document_id))
        if not path.exists(document_path):
            raise DocumentDoesntExistsError(
                    "The {} path doesn't exists, so the document with {} id can't be loaded"
                    "!".format(document_path, document_id))
        else:
            metadata_file = reduce(path.join,
                                   [self._location, str(document_id),
                                    '{}_document_metadata.edd'.format(document_id)])
            meta_data = read_ini_file(metadata_file)
            list_of_files = ([str(file_name.strip("'")) for file_name in
                              meta_data['document']['files'][1:-1].split(', ')])
            if '[' in meta_data['document']['author'] and ']' in meta_data['document']['author']:
                list_of_authors = [int(file_name.strip("'")) for file_name in
                                   meta_data['document']['author'][1:-1].split(', ')]
            else:
                list_of_authors = meta_data['document']['author']
            document = Document(meta_data['document']['title'],
                                meta_data['document']['description'],
                                list_of_authors, list_of_files,
                                meta_data['document']['doc_format'])
            document.creation_date = datetime.strptime(
                    meta_data['document']['creation_date'], '%Y/%m/%d %H:%M:%S %f')
            document.modification_date = datetime.strptime(
                    meta_data['document']['modification_date'],
                    '%Y/%m/%d %H:%M:%S %f')
            document.state = meta_data['document']['state']
            if meta_data['document']['is_public'] == 'True':
                document.make_public()
            return document


    def add_document(self, document):
        new_document_id = get_next_id(self._location)
        new_document_folder = self.create_structure_for_document(new_document_id)
        self.save_document(new_document_folder, new_document_id, document)
        return new_document_id


    def create_structure_for_document(self, new_document_id):
        new_document_folder = path.join(self._location, str(new_document_id))
        makedirs(new_document_folder)
        return new_document_folder


    def update_document(self, document_id, document):
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


    def load_all_documents(self):
        all_documents = dict()
        for document_id in self.find_all_documents():
            all_documents[document_id] = self.load_document(document_id)
        return all_documents


    def find_document_by_id(self, document_id):
        if document_id not in self.find_all_documents():
            raise ValueError(
                    "The document with {} ID doesn't exists, it can't be loaded!".format(document_id))
        else:
            return self.load_all_documents()[document_id]


    def find_documents_by_title(self, title):
        documents_by_title = dict()
        for doc_id_key, doc_value in self.load_all_documents().iteritems():
            if doc_value.title.lower() == title.lower():
                documents_by_title[doc_id_key] = doc_value
        if len(documents_by_title) == 0:
            raise DocumentDoesntExistsError("No document was found with {} title!".format(title))
        else:
            return documents_by_title.values()


    def find_documents_by_author(self, author):
        documents_by_author = dict()
        for doc_id_key, doc_value in self.load_all_documents().iteritems():
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


    def document_files_exist(self, document_id):
        existence_of_document_files = dict()
        if document_id not in self.find_all_documents():
            raise DocumentDoesntExistsError("The docuement with {} ID doesn't exists!".format(document_id))
        else:
            document_path = path.join(self._location, str(document_id))
            document = self.find_document_by_id(document_id)
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
                    print("removed {}".format(file_name_key))
