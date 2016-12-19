#!/usr/bin/env python
""" """

# Imports -----------------------------------------------------------------------------------------------------------
import logging
import random
from os import path, makedirs
from shutil import move

from documents import Document
from generator import DocumentGenerator
from iniformat.writer import write_ini_file
from storage_utils import get_next_id

# Authorship information  -------------------------------------------------------------------------------------------
__author__ = "Zsolt Bokor Levente"
__copyright__ = "Copyright 2016, Morgan Stanley - Training 360 Project"
__credits__ = __author__
__version__ = "1.0.0"
__maintainer__ = __author__
__email__ = ["bokor.zsolt5@gmail.com", "bokorzsolt@yahoo.com"]
__status__ = "Development"

# -------------------------------------------------------------------------------------------------------------------

document_types = ['general', 'office', 'image']
module_logger = logging.getLogger('repository.new_generator')


class NewDocumentGenerator(object):
    def __init__(self, location):
        self._location = location
        if not path.exists(self._location):
            makedirs(self._location)

    def generate_file(self, name):
        doc_generator = DocumentGenerator()
        path_file = path.join(self._location, name)
        doc_generator.generate_random_file(path_file)
        return path_file

    def generate_metadata(self):
        doc_generator = DocumentGenerator()
        return doc_generator.generate_metadata(random.choice(document_types))

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

    def add_document(self, document, new_document_folder = None):
        new_document_id = get_next_id(self._location)
        if not new_document_folder:
            new_document_folder = self.create_structure_for_document(new_document_id)
        self.save_document(new_document_folder, new_document_id, document)
        return new_document_id

    def create_structure_for_document(self, new_document_id):
        new_document_folder = path.join(self._location, str(new_document_id))
        makedirs(new_document_folder)
        return new_document_folder

    def generate_document(self, metadata, authors, files):
        document = Document(metadata['title'], metadata['description'], authors, files, 'txt')
        return self.add_document(document)

    def generate_many_documents(self, number_of_new_doc):
        for _ in xrange(number_of_new_doc):
            document_metadata = self.generate_metadata()
            files = []
            authors = 0
            for _ in range(random.randint(1, 5)):
                new_file_name = self.generate_metadata()['filename']
                files.append(self.generate_file(new_file_name))
            self.generate_document(document_metadata, authors, files)
