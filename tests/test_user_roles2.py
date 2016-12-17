import os
import shutil
import unittest
from datetime import date
from os import makedirs, path

from repository import Repository
from users import User


class TestUserRoles(unittest.TestCase):
    """Test the user role functions"""


    def setUp(self):
        makedirs('/DevTest/edms/users')
        repo = Repository()
        # self._user_manager = UserManager('/DevTest/edms/users')
        self._user_manager = repo._user_manager
        # self._role_path = RoleManager.get_roles_file(repo._location)
        self._role_path = '/DevTest/edms/users/roles.txt'


    def tearDown(self):
        shutil.rmtree('/DevTest/edms')
        shutil.rmtree(path.join('Repositories', 'repo_1'))

    def test_create_new_role_file(self):
        self._user_manager.set_role_file(self._role_path)
        self.assertTrue(os.path.exists(self._role_path))


    def test_set_empty_role_file(self):
        with open(self._role_path, 'w') as role_file:
            os.utime(self._role_path, None)
        self._user_manager.set_role_file(self._role_path)


    def test_check_empty_role_file(self):
        with open(self._role_path, 'w') as role_file:
            os.utime(self._role_path, None)
        self._user_manager.check_role_file(self._role_path)


    def test_check_one_role(self):
        with open(self._role_path, 'w') as role_file:
            role_file.write('1: admin')
        self._user_manager.check_role_file(self._role_path)


    def test_check_three_roles(self):
        with open(self._role_path, 'w') as role_file:
            role_file.write('1: admin,manager,author')
        self._user_manager.check_role_file(self._role_path)


    def test_check_two_users(self):
        with open(self._role_path, 'w') as role_file:
            role_file.write('1: admin\n')
            role_file.write('2: author\n')
        self._user_manager.check_role_file(self._role_path)


    def test_check_multiple_users_and_roles(self):
        with open(self._role_path, 'w') as role_file:
            role_file.write('1: admin,manager\n')
            role_file.write('2: author,reviewer\n')
            role_file.write('3: reviewer\n')
        self._user_manager.check_role_file(self._role_path)


    def test_check_missing_identifier(self):
        with open(self._role_path, 'w') as role_file:
            role_file.write('1: admin,manager\n')
            role_file.write(': author,reviewer\n')
            role_file.write('3: reviewer\n')
        with self.assertRaises(ValueError):
            self._user_manager.check_role_file(self._role_path)


    def test_check_missing_colon(self):
        with open(self._role_path, 'w') as role_file:
            role_file.write('1: admin,manager\n')
            role_file.write('2 author,reviewer\n')
            role_file.write('3: reviewer\n')
        with self.assertRaises(ValueError):
            self._user_manager.check_role_file(self._role_path)


    def test_invalid_role_name(self):
        with open(self._role_path, 'w') as role_file:
            role_file.write('1: admin,manager\n')
            role_file.write('2: observer,reviewer\n')
            role_file.write('3: reviewer\n')
        with self.assertRaises(ValueError):
            self._user_manager.check_role_file(self._role_path)


    def test_too_many_commas(self):
        with open(self._role_path, 'w') as role_file:
            role_file.write('1: admin,manager\n')
            role_file.write('2: author,,reviewer\n')
            role_file.write('3: reviewer\n')
        with self.assertRaises(ValueError):
            self._user_manager.check_role_file(self._role_path)


    def test_missing_comma(self):
        with open(self._role_path, 'w') as role_file:
            role_file.write('1: admin,manager\n')
            role_file.write('2: author reviewer\n')
            role_file.write('3: reviewer\n')
        with self.assertRaises(ValueError):
            self._user_manager.check_role_file(self._role_path)


    def test_duplicated_user_id(self):
        with open(self._role_path, 'w') as role_file:
            role_file.write('1: admin,manager\n')
            role_file.write('2: author,reviewer\n')
            role_file.write('1: reviewer\n')
        with self.assertRaises(ValueError):
            self._user_manager.check_role_file(self._role_path)


    def test_duplicated_role(self):
        with open(self._role_path, 'w') as role_file:
            role_file.write('1: admin,manager,admin\n')
            role_file.write('2: author,reviewer\n')
            role_file.write('3: reviewer\n')
        with self.assertRaises(ValueError):
            self._user_manager.check_role_file(self._role_path)


    def test_adding_role(self):
        user = User('First', 'Family', date(1990, 12, 1), 'user@mail.com', '1234')
        user_id = self._user_manager.add_user(user)
        self._user_manager.add_role(user_id, 'manager')
        is_manager = self._user_manager.has_role(user_id, 'manager')
        self.assertTrue(is_manager)


    def test_adding_multiple_roles(self):
        user = User('First', 'Family', date(1990, 12, 1), 'user@mail.com', '1234')
        user_id = self._user_manager.add_user(user)
        self._user_manager.add_role(user_id, 'manager')
        self._user_manager.add_role(user_id, 'reviewer')
        is_reviewer = self._user_manager.has_role(user_id, 'reviewer')
        is_manager = self._user_manager.has_role(user_id, 'manager')
        is_admin = self._user_manager.has_role(user_id, 'admin')
        self.assertTrue(is_manager)
        self.assertTrue(is_reviewer)
        self.assertFalse(is_admin)


    def test_adding_invalid_role(self):
        user = User('First', 'Family', date(1990, 12, 1), 'user@mail.com', '1234')
        user_id = self._user_manager.add_user(user)
        with self.assertRaises(ValueError):
            self._user_manager.add_role(user_id, 'invalid')


    def test_adding_role_with_invalid_id(self):
        with self.assertRaises(ValueError):
            self._user_manager.add_role(10, 'author')


    def test_add_role_multiple_times(self):
        user = User('First', 'Family', date(1990, 12, 1), 'user@mail.com', '1234')
        user_id = self._user_manager.add_user(user)
        self._user_manager.add_role(user_id, 'author')
        self._user_manager.add_role(user_id, 'author')
        self.assertTrue(self._user_manager.has_role(user_id, 'author'))
        self._user_manager.remove_role(user_id, 'author')
        self.assertFalse(self._user_manager.has_role(user_id, 'author'))


    def test_removing_role(self):
        user = User('First', 'Family', date(1990, 12, 1), 'user@mail.com', '1234')
        user_id = self._user_manager.add_user(user)
        self._user_manager.add_role(user_id, 'author')
        self.assertTrue(self._user_manager.has_role(user_id, 'author'))
        self._user_manager.remove_role(user_id, 'author')
        self.assertFalse(self._user_manager.has_role(user_id, 'author'))


    def test_removing_invalid_role(self):
        user = User('First', 'Family', date(1990, 12, 1), 'user@mail.com', '1234')
        user_id = self._user_manager.add_user(user)
        with self.assertRaises(ValueError):
            self._user_manager.remove_role(user_id, 'invalid')


    def test_removing_role_with_invalid_id(self):
        with self.assertRaises(ValueError):
            self._user_manager.remove_role(10, 'author')


    def test_removing_role_multiple_time(self):
        user = User('First', 'Family', date(1990, 12, 1), 'user@mail.com', '1234')
        user_id = self._user_manager.add_user(user)
        self._user_manager.add_role(user_id, 'author')
        self.assertTrue(self._user_manager.has_role(user_id, 'author'))
        for i in range(10):
            self._user_manager.remove_role(user_id, 'author')
            self.assertFalse(self._user_manager.has_role(user_id, 'author'))


    def test_find_users_by_role_empty(self):
        users = self._user_manager.find_users_by_role('author')
        self.assertEqual(len(users), 0)


    def test_find_users_by_invalid_role(self):
        with self.assertRaises(ValueError):
            self._user_manager.find_users_by_role('invalid')


    def test_find_users_by_role_one_result(self):
        user = User('First', 'Family', date(1990, 12, 1), 'user@mail.com', '1234')
        user_id = self._user_manager.add_user(user)
        self._user_manager.add_role(user_id, 'author')
        authors = self._user_manager.find_users_by_role('author')
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0].first_name, 'First')


    def test_find_users_by_role_multiple_results(self):
        a = User('A', 'Family', date(1990, 12, 1), 'a@mail.com', '1234')
        b = User('B', 'Family', date(1990, 12, 2), 'b@mail.com', '1234')
        c = User('C', 'Family', date(1990, 12, 3), 'c@mail.com', '1234')
        a_id = self._user_manager.add_user(a)
        b_id = self._user_manager.add_user(b)
        c_id = self._user_manager.add_user(c)
        self._user_manager.add_role(a_id, 'author')
        self._user_manager.add_role(c_id, 'author')
        self._user_manager.add_role(b_id, 'reviewer')
        self._user_manager.add_role(c_id, 'reviewer')
        admins = self._user_manager.find_users_by_role('admin')
        authors = self._user_manager.find_users_by_role('author')
        reviewers = self._user_manager.find_users_by_role('reviewer')
        self.assertEqual(len(admins), 0)
        self.assertEqual(len(authors), 2)
        self.assertEqual(len(reviewers), 2)
