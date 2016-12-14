import unittest
from datetime import date

from users import User

SKIP_ADVANCED = False


class TestUser(unittest.TestCase):
    """Test the user class"""


    def test_creation(self):
        user = User('First', 'Family', date(1990, 12, 1), 'user@mail.com', '1234')


    def test_properties(self):
        user = User('First', 'Family', date(1990, 12, 1), 'user@mail.com', '1234')
        self.assertEqual(user.first_name, 'First')
        self.assertEqual(user.family_name, 'Family')
        self.assertEqual(user.birth, date(1990, 12, 1))
        self.assertEqual(user.email, 'user@mail.com')
        self.assertEqual(user.password, '1234')


    @unittest.skipIf(SKIP_ADVANCED, 'The email validation is an advanced task.')
    def test_email_validation(self):
        with self.assertRaises(ValueError):
            user = User('First', 'Family', date(1990, 12, 1), 'user.mail.com', '1234')
