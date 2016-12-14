import unittest

from documents import Document


class TestDocument(unittest.TestCase):
    """Test the document class"""


    def test_creation(self):
        document = Document('title1', 'desc1', 1, ['1.pdf', '2.pdf'], 'pdf')


    def test_properties(self):
        document = Document('title1', 'desc1', 1, ['1.pdf', '2.pdf'], 'pdf')
        self.assertEqual(document.title, 'title1')
        self.assertEqual(document.description, 'desc1')
        self.assertEqual(document.author, 1)
        self.assertEqual(document.files, ['1.pdf', '2.pdf'])
        self.assertEqual(document.doc_format, 'pdf')


    def test_visibility(self):
        document = Document('title1', 'desc1', 1, ['1.pdf', '2.pdf'], 'pdf')
        self.assertFalse(document.is_public())
        document.make_public()
        self.assertTrue(document.is_public())
        document.make_private()
        self.assertFalse(document.is_public())


    def test_initial_state(self):
        document = Document('title1', 'desc1', 1, ['1.pdf', '2.pdf'], 'pdf')
        self.assertEqual(document.state, 'new')


    def test_accept_document(self):
        document = Document('title1', 'desc1', 1, ['1.pdf', '2.pdf'], 'pdf')
        document.change_state('pending')
        document.change_state('accepted')
        self.assertEqual(document.state, 'accepted')


    def test_reject_document(self):
        document = Document('title1', 'desc1', 1, ['1.pdf', '2.pdf'], 'pdf')
        document.change_state('pending')
        document.change_state('rejected')
        self.assertEqual(document.state, 'rejected')


    def test_invalid_accept(self):
        document = Document('title1', 'desc1', 1, ['1.pdf', '2.pdf'], 'pdf')
        with self.assertRaises(ValueError):
            document.change_state('accepted')


    def test_invalid_reject(self):
        document = Document('title1', 'desc1', 1, ['1.pdf', '2.pdf'], 'pdf')
        with self.assertRaises(ValueError):
            document.change_state('rejected')


    def test_invalid_new_state(self):
        document = Document('title1', 'desc1', 1, ['1.pdf', '2.pdf'], 'pdf')
        document.change_state('pending')
        with self.assertRaises(ValueError):
            document.change_state('new')


    def test_public_visibility(self):
        document = Document('title1', 'desc1', 1, ['1.pdf', '2.pdf'], 'pdf')
        document.make_public()
        self.assertTrue(document.is_public())


    def test_private_visibility(self):
        document = Document('title1', 'desc1', 1, ['1.pdf', '2.pdf'], 'pdf')
        document.make_private()
        self.assertFalse(document.is_public())
