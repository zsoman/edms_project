import shutil
import unittest
from os import path, makedirs

from docgen import generator
from documents import Document
from documents import DocumentManager


class TestDocumentManager(unittest.TestCase):
    """Test the document manager class"""


    def setUp(self):
        makedirs('/tmp/edms/documents')
        document_generator = generator.DocumentGenerator()
        makedirs('/tmp/edms/samples')
        for name in ['a1.pdf', 'a2.pdf', 'b.doc', 'c1.html', 'c2.png', 'c3.png', 'c1.pdf',
                     'c2.pdf', 'c3.pdf']:
            if not path.exists('/tmp/edms/samples'):
                makedirs('/tmp/edms/samples')
            document_generator.generate_random_file('/tmp/edms/samples/{}'.format(name))
        self._document_manager = DocumentManager('/tmp/edms/documents')


    def tearDown(self):
        shutil.rmtree('/tmp/edms')


    def test_empty_document_storage(self):
        document_count = self._document_manager.count_documents()
        self.assertEqual(document_count, 0)


    def test_add_document(self):
        document = Document('title1', 'desc1', 1, ['/tmp/edms/samples/a1.pdf', '/tmp/edms/samples/a2.pdf'],
                            'pdf')
        self._document_manager.add_document(document)
        self.assertEqual(self._document_manager.count_documents(), 1)


    def test_multiple_document_addition(self):
        for i in range(100):
            document = Document('Title {}'.format(i), 'Desc {}'.format(i), 1,
                                ['/tmp/edms/samples/a1.pdf', '/tmp/edms/samples/a2.pdf'], 'pdf')
            document_generator = generator.DocumentGenerator()
            for name in ['a1.pdf', 'a2.pdf', 'b.doc', 'c1.html', 'c2.png', 'c3.png', 'c1.pdf',
                         'c2.pdf', 'c3.pdf']:
                if not path.exists('/tmp/edms/samples'):
                    makedirs('/tmp/edms/samples')
                document_generator.generate_random_file('/tmp/edms/samples/{}'.format(name))
            self._document_manager.add_document(document)
        self.assertEqual(self._document_manager.count_documents(), 100)


    def test_retrieve_last_document(self):
        document = Document('title1', 'desc1', 1,
                            ['/tmp/edms/samples/a1.pdf', '/tmp/edms/samples/a2.pdf'],
                            'pdf')
        document_id = self._document_manager.add_document(document)
        retrieved = self._document_manager.find_document_by_id(document_id)
        self.assertEqual(retrieved.title, 'title1')
        self.assertEqual(retrieved.description, 'desc1')
        self.assertEqual(retrieved.author, 1)
        self.assertEqual(retrieved.files, ['a1.pdf', 'a2.pdf'])
        self.assertEqual(retrieved.doc_format, 'pdf')


    def test_find_document_by_id(self):
        a = Document('A', 'description of A', 1,
                     ['/tmp/edms/samples/a1.pdf', '/tmp/edms/samples/a2.pdf'], 'pdf')
        b = Document('B', 'description of B', 2, ['/tmp/edms/samples/b.doc'], 'doc')
        c = Document('C', 'description of C', 1,
                     ['/tmp/edms/samples/c1.html', '/tmp/edms/samples/c2.png',
                      '/tmp/edms/samples/c3.png'], 'html')
        a_id = self._document_manager.add_document(a)
        b_id = self._document_manager.add_document(b)
        c_id = self._document_manager.add_document(c)
        document = self._document_manager.find_document_by_id(c_id)
        self.assertEqual(document.title, 'C')
        document = self._document_manager.find_document_by_id(b_id)
        self.assertEqual(document.title, 'B')
        document = self._document_manager.find_document_by_id(a_id)
        self.assertEqual(document.title, 'A')


    def test_invalid_id_in_empty(self):
        with self.assertRaises(ValueError):
            self._document_manager.find_document_by_id(1234)


    def test_invalid_id(self):
        a = Document('title1', 'desc1', 1,
                     ['/tmp/edms/samples/a1.pdf', '/tmp/edms/samples/a2.pdf'], 'pdf')
        a_id = self._document_manager.add_document(a)
        with self.assertRaises(ValueError):
            self._document_manager.find_document_by_id(a_id + 1)


    def test_document_update(self):
        a = Document('A', 'description of A', 1,
                     ['/tmp/edms/samples/a1.pdf', '/tmp/edms/samples/a2.pdf'], 'pdf')
        document_id = self._document_manager.add_document(a)
        b = Document('B', 'description of B', 2, ['/tmp/edms/samples/b.doc'], 'doc')
        self._document_manager.update_document(document_id, b)
        updated_document = self._document_manager.find_document_by_id(document_id)
        self.assertEqual(updated_document.author, b.author)
        self.assertEqual(updated_document.doc_format, b.doc_format)


    def test_document_update_with_invalid_id(self):
        with self.assertRaises(ValueError):
            a = Document('A', 'description of A', 1,
                         ['/tmp/edms/samples/a1.pdf', '/tmp/edms/samples/a2.pdf'], 'pdf')
            document_id = self._document_manager.add_document(a)
            b = Document('B', 'description of B', 2, ['/tmp/edms/samples/b.doc'], 'doc')
            # sleep(1000)
            self._document_manager.update_document(document_id + 1, b)


    def test_document_remove(self):
        a = Document('A', 'description of A', 1, ['/tmp/edms/samples/a1.pdf', '/tmp/edms/samples/a2.pdf'],
                     'pdf')
        a_id = self._document_manager.add_document(a)
        b = Document('B', 'description of B', 2, ['/tmp/edms/samples/b.doc'], 'doc')
        b_id = self._document_manager.add_document(b)
        self.assertEqual(self._document_manager.count_documents(), 2)
        self._document_manager.remove_document(a_id)
        # sleep(1000)
        document = self._document_manager.find_document_by_id(b_id)
        self.assertEqual(document.title, 'B')
        self.assertEqual(self._document_manager.count_documents(), 1)


    def test_document_remove_with_invalid_id(self):
        a = Document('A', 'description of A', 1,
                     ['/tmp/edms/samples/a1.pdf', '/tmp/edms/samples/a2.pdf'], 'pdf')
        a_id = self._document_manager.add_document(a)
        with self.assertRaises(ValueError):
            self._document_manager.remove_document(a_id + 1)


    def test_find_document_by_title(self):
        a = Document('A', 'description of A', 1,
                     ['/tmp/edms/samples/a1.pdf', '/tmp/edms/samples/a2.pdf'], 'pdf')
        self._document_manager.add_document(a)
        b = Document('B', 'description of B', 2, ['/tmp/edms/samples/b.doc'], 'doc')
        self._document_manager.add_document(b)
        documents = self._document_manager.find_documents_by_title('a')
        self.assertEqual(len(documents), 1)
        document = documents[0]
        self.assertEqual(a.title, document.title)
        self.assertEqual(a.description, document.description)
        self.assertEqual(a.author, document.author)
        self.assertEqual(document.files, ['a1.pdf', 'a2.pdf'])
        self.assertEqual(a.doc_format, document.doc_format)


    def test_find_documents_by_author(self):
        a = Document('A', 'description of A', 1,
                     ['/tmp/edms/samples/a1.pdf', '/tmp/edms/samples/a2.pdf'], 'pdf')
        self._document_manager.add_document(a)
        b = Document('B', 'description of B', 2, ['/tmp/edms/samples/b.doc'], 'doc')
        self._document_manager.add_document(b)
        documents = self._document_manager.find_documents_by_author(1)
        self.assertEqual(len(documents), 1)
        document = documents[0]
        self.assertEqual(a.title, document.title)
        self.assertEqual(a.description, document.description)
        self.assertEqual(a.author, document.author)
        self.assertEqual(document.files, ['a1.pdf', 'a2.pdf'])
        self.assertEqual(a.doc_format, document.doc_format)


    def test_find_documents_by_format(self):
        a = Document('A', 'description of A', 1,
                     ['/tmp/edms/samples/a1.pdf', '/tmp/edms/samples/a2.pdf'], 'pdf')
        b = Document('B', 'description of B', 2, ['/tmp/edms/samples/b.doc'], 'doc')
        c = Document('C', 'description of A', 1,
                     ['/tmp/edms/samples/c1.pdf', '/tmp/edms/samples/c2.pdf',
                      '/tmp/edms/samples/c3.pdf'], 'pdf')
        self._document_manager.add_document(a)
        self._document_manager.add_document(b)
        self._document_manager.add_document(c)
        documents = self._document_manager.find_documents_by_format('pdf')
        self.assertEqual(len(documents), 2)
        titles = {document.title for document in documents}
        self.assertIn('A', titles)
        self.assertIn('C', titles)
