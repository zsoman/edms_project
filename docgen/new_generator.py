import random
from os import path, makedirs, listdir, remove
from shutil import rmtree

from documents import Document
from documents import DocumentManager
from generator import DocumentGenerator
from iniformat.reader import read_ini_file
from usergen.generator import UserGenerator
from users import User, UserManager

document_types = ['general', 'office', 'image']


class NewDocumentGenerator(object):
    def __init__(self, repo, user_manager, doc_manager):
        self._location = path.join(repo._location, 'sample')
        self._user_manager = UserManager(self._location)
        self._doc_manager = DocumentManager(self._location)
        if not path.exists(self._location):
            makedirs(self._location)


    # def save_documents_to_repository(self):
    #     all_documents = self._document_manager.find_all_documents()
    #     for document in all_documents:
    #         metadata_data = read_ini_file(self._repository._paths_file)
    #         mew_path = path.join(self._repository._location, metadata_data['directories']['documents'])
    #         move(path.join(self._location, document), mew_path)

    def generate_author(self):
        user_generator = UserGenerator()

        fname = user_generator.generate_first_name()
        lname = user_generator.generate_family_name()
        birth = user_generator.generate_birth_date()
        email = user_generator.generate_email(fname, lname)
        password = user_generator.generate_password()

        user = User(fname, lname, birth, email, password)
        return self._user_manager.add_user(user)


    def generate_file(self, name):
        doc_generator = DocumentGenerator()
        path_file = path.join(self._location, name)
        doc_generator.generate_random_file(path_file)
        return path_file


    def generate_metadata(self):
        doc_generator = DocumentGenerator()
        return doc_generator.generate_metadata(random.choice(document_types))


    def generate_document(self, metadata, authors, files):
        document = Document(metadata['title'], metadata['description'], authors, files, 'txt')
        doc_id = self._doc_manager.add_document(document)
        return read_ini_file(
                reduce(path.join,
                       [self._doc_manager._location, str(doc_id), '{}_document_metadata.edd'.format(doc_id)]))


    def generate_many_documents(self, number_of_new_doc):
        for _ in xrange(number_of_new_doc):
            document_metadata = self.generate_metadata()
            files = []
            authors = []
            for _ in range(random.randint(1, 5)):
                new_file_name = self.generate_metadata()['filename']
                files.append(self.generate_file(new_file_name))
            for _ in range(random.randint(1, 5)):
                authors.append(self.generate_author())
            self.generate_document(document_metadata, authors, files)

        for file_or_folder in listdir(self._location):
            full_path_file_or_folder = path.join(self._location, file_or_folder)
            if path.isdir(full_path_file_or_folder):
                if file_or_folder not in ['documents', 'users']:
                    rmtree(full_path_file_or_folder)
            else:
                remove(full_path_file_or_folder)
