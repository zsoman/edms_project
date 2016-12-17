import shutil
import unittest
from datetime import date
from os import makedirs

from repository import Repository
from users import User

SKIP_ADVANCED = False


class TestUserManager(unittest.TestCase):
    """Test the user manager class"""


    def setUp(self):
        makedirs('/tmp/edms/users')
        repo = Repository('/tmp/edms')
        # self._user_manager = UserManager('/tmp/edms/users')
        self._user_manager = repo._user_manager


    def tearDown(self):
        shutil.rmtree('/tmp/edms')
        shutil.rmtree('Repositories')

    def test_empty_user_storage(self):
        user_count = self._user_manager.count_users()
        self.assertEqual(user_count, 0)


    def test_add_user(self):
        user = User('First', 'Family', date(1990, 12, 1), 'user@mail.com', '1234')
        self._user_manager.add_user(user)
        self.assertEqual(self._user_manager.count_users(), 1)


    def test_multiple_user_addition(self):
        """This test case is wrong! The user name couldn't contain numbers. The task says explicitly that all data
        should be check before the object creation, fails because I check that a name can only be alphanumeric."""
        for i in range(1950, 2000):
            user = User('User{}'.format(i), 'Family', date(i, 12, 1), 'user@mail.com', '{}'.format(i))
            self._user_manager.add_user(user)
        self.assertEqual(self._user_manager.count_users(), 50)


    def test_retrieve_last_user(self):
        user = User('First', 'Family', date(1990, 12, 1), 'user@mail.com', '1234')
        user_id = self._user_manager.add_user(user)
        retrieved = self._user_manager.find_user_by_id(user_id)
        self.assertEqual(user.first_name, retrieved.first_name)
        self.assertEqual(user.family_name, retrieved.family_name)
        self.assertEqual(user.birth, retrieved.birth)
        self.assertEqual(user.email, retrieved.email)
        self.assertEqual(user.password, retrieved.password)


    def test_find_user_by_id(self):
        a = User('A', 'Family', date(1990, 12, 1), 'a@mail.com', '1234')
        b = User('B', 'Family', date(1990, 12, 2), 'b@mail.com', '1234')
        c = User('C', 'Family', date(1990, 12, 3), 'c@mail.com', '1234')
        a_id = self._user_manager.add_user(a)
        b_id = self._user_manager.add_user(b)
        c_id = self._user_manager.add_user(c)
        user = self._user_manager.find_user_by_id(c_id)
        self.assertEqual(user.first_name, 'C')
        user = self._user_manager.find_user_by_id(b_id)
        self.assertEqual(user.first_name, 'B')
        user = self._user_manager.find_user_by_id(a_id)
        self.assertEqual(user.first_name, 'A')


    def test_invalid_id_in_empty(self):
        with self.assertRaises(ValueError):
            self._user_manager.find_user_by_id(1234)


    def test_invalid_id(self):
        a = User('A', 'Family', date(1990, 12, 1), 'a@mail.com', '1234')
        a_id = self._user_manager.add_user(a)
        with self.assertRaises(ValueError):
            self._user_manager.find_user_by_id(a_id + 1)


    def test_user_update(self):
        a = User('A', 'Family', date(1990, 12, 1), 'a@mail.com', '1234')
        user_id = self._user_manager.add_user(a)
        b = User('B', 'Family', date(1990, 12, 2), 'b@mail.com', '1234')
        self._user_manager.update_user(user_id, b)
        updated_user = self._user_manager.find_user_by_id(user_id)
        self.assertEqual(updated_user.first_name, b.first_name)
        self.assertEqual(updated_user.email, b.email)


    def test_user_update_with_invalid_id(self):
        with self.assertRaises(ValueError):
            a = User('A', 'Family', date(1990, 12, 1), 'a@mail.com', '1234')
            user_id = self._user_manager.add_user(a)
            b = User('B', 'Family', date(1990, 12, 2), 'b@mail.com', '1234')
            self._user_manager.update_user(user_id + 1, b)


    def test_user_remove(self):
        a = User('A', 'Family', date(1990, 12, 1), 'a@mail.com', '1234')
        a_id = self._user_manager.add_user(a)
        b = User('B', 'Family', date(1990, 12, 2), 'b@mail.com', '1234')
        b_id = self._user_manager.add_user(b)
        self.assertEqual(self._user_manager.count_users(), 2)
        self._user_manager.remove_user(a_id)
        user = self._user_manager.find_user_by_id(b_id)
        self.assertEqual(user.first_name, 'B')
        self.assertEqual(self._user_manager.count_users(), 1)


    def test_user_remove_with_invalid_id(self):
        a = User('A', 'Family', date(1990, 12, 1), 'a@mail.com', '1234')
        a_id = self._user_manager.add_user(a)
        with self.assertRaises(ValueError):
            self._user_manager.remove_user(a_id + 1)


    @unittest.skipIf(SKIP_ADVANCED, 'This is an advanced task.')
    def test_find_users_by_name(self):
        a = User('Alexander', 'HUGHES', date(1990, 12, 1), 'a@mail.com', '1234')
        self._user_manager.add_user(a)
        b = User('Bruce', 'Butler', date(1990, 12, 2), 'b@mail.com', '****')
        self._user_manager.add_user(b)
        c = User('Cheryl', 'Parker', date(1990, 12, 3), 'c@mail.com', 'admin')
        self._user_manager.add_user(c)
        result = self._user_manager.find_users_by_name('er')
        self.assertEqual(len(result), 3)
        result = self._user_manager.find_users_by_name('he')
        self.assertEqual(len(result), 2)
        result = self._user_manager.find_users_by_name('alex')
        self.assertEqual(len(result), 1)
        result = self._user_manager.find_users_by_name('PARKER')
        self.assertEqual(len(result), 1)
        result = self._user_manager.find_users_by_name('NOT-FOUND')
        self.assertEqual(len(result), 0)


    @unittest.skipIf(SKIP_ADVANCED, 'This is an advanced task.')
    def test_find_users_by_email(self):
        a = User('Alexander', 'Hughes', date(1990, 12, 1), 'a.hughes@mail.com', '1234')
        self._user_manager.add_user(a)
        b = User('Bruce', 'Butler', date(1990, 12, 2), 'brrr@mail.org', '****')
        self._user_manager.add_user(b)
        c = User('Cheryl', 'Parker', date(1990, 12, 3), 'cheryl576@mail.gov', 'admin')
        self._user_manager.add_user(c)
        result = self._user_manager.find_users_by_email('mail')
        self.assertEqual(len(result), 3)
        result = self._user_manager.find_users_by_email('gov')
        self.assertEqual(len(result), 1)
        result = self._user_manager.find_users_by_email('HUG')
        self.assertEqual(len(result), 1)
        result = self._user_manager.find_users_by_email('postfix')
        self.assertEqual(len(result), 0)
