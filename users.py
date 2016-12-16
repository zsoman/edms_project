"""Managing of user data

The data of the users are stored in the users directory (by default).

The file names are the identifiers of the users.

A new user identifier is generated by finding the maximal value of the identifiers and increasing by one.

The fields of a user object stored in the text file line-by-line as:

    first_name
    family_name
    birth
    email
    password

"""

import xml.etree.ElementTree as ET
from collections import defaultdict, Counter
from datetime import datetime, date
from json import load, dump
from os import path, remove, listdir
from re import match
from shutil import move

import storage_utils
from iniformat.reader import read_ini_file

DELIMITER_CHAR = ':'
ROLE_DELIMITER_CHAR = ','


class UserNotFoundError(Exception):
    pass


class WrongFileTypeError(Exception):
    pass


class MissingUserIdentifierError(Exception):
    pass


class MissingDelimiterCharacterError(Exception):
    pass


class InvalidRoleNameError(Exception):
    pass


class InconsistentUseOfRoleDelimiterError(Exception):
    pass


class DuplicateUserIdentifierError(Exception):
    pass


class DuplicatedRolesError(Exception):
    pass


class User(object):
    """User of the document repository"""


    def __init__(self, first_name, family_name, birth, email, password):
        if User.is_valid_name(first_name):
            self._first_name = first_name
        else:
            raise TypeError("The {} first name is not a valid name!".format(first_name))

        if User.is_valid_name(family_name):
            self._family_name = family_name
        else:
            raise TypeError("The {} family name is not a valid name!".format(family_name))

        if User.is_valid_date(birth):
            self._birth = birth
        else:
            raise TypeError("The {} birt date is not a valid date!".format(birth))

        if User.is_valid_email(email):
            self._email = email
        else:
            raise ValueError(
                    "The {} email address is not a valid email address!".format(email))

        if User.is_valid_password(password):
            self._password = password
        else:
            raise TypeError("The {} password is not a valid string!".format(password))


    @classmethod
    def is_valid_name(cls, name):
        return name.isalnum()


    @classmethod
    def is_valid_date(cls, date_obj):
        return isinstance(date_obj, date)


    @classmethod
    def is_valid_email(cls, email):
        return match(
                '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                email)


    @classmethod
    def is_valid_password(cls, password):
        for char in password:
            if not isinstance(char, str):
                return False
        return True


    @property
    def first_name(self):
        return self._first_name


    @property
    def family_name(self):
        return self._family_name


    @property
    def full_name(self):
        return self._first_name + ' ' + self._family_name


    @property
    def birth(self):
        return self._birth


    @property
    def email(self):
        return self._email


    @property
    def password(self):
        return self._password


    def __str__(self):
        return '{} {} {} {}'.format(self.full_name, self.birth, self.email, self.password)


class Role(object):
    """Represents the roles of the users"""


    def __init__(self, role):
        if role in ['admin', 'manager', 'author', 'reviewer', 'visitor', '']:
            self._role = role
        else:
            raise ValueError("The '{}' is an invalid role!".format(role))


    @property
    def role(self):
        return self._role


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._role == other._role
        return False


    def __str__(self):
        return self._role


class RoleManager(object):
    """Manage the user roles which are stored in a text file."""


    def __init__(self, repository_location, paths_file):
        metadata_data = read_ini_file(paths_file)
        self._location = path.join(repository_location, metadata_data['directories']['users'])


    def read_roles(self):
        """Read roles from the file."""
        return RoleManager.parse_roles_file(path.join(self._location, RoleManager.get_roles_file(self._location)))


    def write_roles(self, users_roles):
        """Write roles to the file."""

        roles_file = path.join(self._location, RoleManager.get_roles_file(self._location))
        if roles_file.endswith('txt'):
            with open(roles_file, 'w') as file_obj:
                for id_key, roles_value in users_roles.iteritems():
                    roles_str = ''
                    for role in roles_value:
                        roles_str += '{},'.format(role)
                    file_obj.write('{}: {}\n'.format(id_key, roles_str[:-1]))

        elif roles_file.endswith('json'):
            existing_users_roles = self.read_roles()
            with open(roles_file, 'w') as file_obj:
                existing_users_roles.update(users_roles)
                serializable_existing_users_roles = dict()
                for id_key, roles_value in existing_users_roles.iteritems():
                    serializable_roles = []
                    for role_obj in roles_value:
                        serializable_roles.append(role_obj.role)
                    serializable_existing_users_roles[id_key] = serializable_roles
                dump(serializable_existing_users_roles, file_obj)

        elif roles_file.endswith('xml'):
            existing_users_roles = self.read_roles()
            existing_users_roles.update(users_roles)
            root = ET.Element('users')
            for id_key, roles_value in existing_users_roles.iteritems():
                user = ET.SubElement(root, 'user')
                user.set('id', str(id_key))
                for role in roles_value:
                    role_element = ET.SubElement(user, 'role')
                    role_element.text = role
            tree = ET.ElementTree(root)
            tree.write(roles_file)


    @classmethod
    def get_roles_file(cls, folder_path):
        number_of_role_files = 0
        for file in listdir(folder_path):
            if file.startswith('roles'):
                if number_of_role_files > 0:
                    raise RuntimeError("Multiple roles file in the repository!")
                elif file.split('.')[1] not in ['txt', 'json', 'xml']:
                    raise TypeError(
                            "Inappropriate file extinsion of {} file, it should be TXT, JSON or XML!".format(
                                    file))
                else:
                    return file


    @classmethod
    def parse_roles_file(cls, roles_file):
        with open(roles_file) as file_obj:
            if file_obj.readline() == '':
                return dict()
        if roles_file.endswith('txt'):
            with open(roles_file) as file_obj:
                users_roles = dict()
                for line in file_obj:
                    row = line.split(':')
                    user_id = int(row[0].strip())
                    raw_roles = row[1].strip().split(',')
                    user_roles = []
                    for role in raw_roles:
                        user_roles.append(Role(role.strip()))
                    users_roles[user_id] = user_roles
            return users_roles

        elif roles_file.endswith('json'):
            users_roles = dict()
            with open(roles_file) as file_obj:
                data = load(file_obj)
            for id_key, roles_value in data.iteritems():
                user_roles = []
                for r in roles_value:
                    user_roles.append(Role(r))
                users_roles[int(id_key)] = user_roles
            return users_roles

        elif roles_file.endswith('xml'):
            tree = ET.parse(roles_file)
            users_root = tree.getroot()
            users_roles = dict()
            for user in users_root:
                user_id = int(user.attrib['id'])
                user_roles = []
                for role in user:
                    user_roles.append(Role(role.text))
                users_roles[user_id] = user_roles
            return users_roles

        else:
            raise WrongFileTypeError(
                    "The {} file's type is inappropriate it should be TXT, JSON or XML!".format(roles_file))


class UserManager(object):
    """Manage user objects"""


    def __init__(self, repository_location, paths_file):
        self.paths_file = paths_file
        self.repository_location = repository_location
        metadata_data = read_ini_file(self.paths_file)
        self._location = path.join(self.repository_location, metadata_data['directories']['users'])


    def save_user(self, user_id, user):
        """Save user to file"""
        with open(path.join(self._location, str(user_id)), 'w') as user_file:
            user_file.write(user.first_name + '\n')
            user_file.write(user.family_name + '\n')
            user_file.write(str(user.birth) + '\n')
            user_file.write(user.email + '\n')
            user_file.write(''.join(user.password) + '\n')


    def load_user(self, user_id):
        """Load user from file"""
        with open(path.join(self._location, str(user_id))) as user_file:
            first_name = user_file.readline().rstrip('\n')
            family_name = user_file.readline().rstrip('\n')
            birth = datetime.strptime(user_file.readline().rstrip('\n'), "%Y-%m-%d").date()
            email = user_file.readline().rstrip('\n')
            password = user_file.readline().rstrip('\n')
        user = User(first_name, family_name, birth, email, password)
        return user


    def add_user(self, user):
        user_id = storage_utils.get_next_id(self._location)
        self.save_user(user_id, user)
        return user_id


    def update_user(self, user_id, user):
        self.remove_user(user_id)
        self.save_user(user_id, user)


    def remove_user(self, user_id):
        user_file_path = path.join(self._location, str(user_id))
        if path.exists(user_file_path):
            remove(user_file_path)
        else:
            raise ValueError('The user id {} does not exist!'.format(user_id))


    def find_user_by_id(self, user_id):
        user_file_path = path.join(self._location, str(user_id))
        if path.exists(user_file_path):
            user = self.load_user(user_id)
            return user
        else:
            raise ValueError('The user id {} does not exist!'.format(user_id))


    def find_users_by_name(self, name):
        all_files = UserManager.all_files_in_folder(self._location)
        found_users = []
        for user_file in all_files:
            with open(path.join(self._location, user_file)) as file_obj:
                first_name = file_obj.readline().strip()
                family_name = file_obj.readline().strip()
                if name.lower() in '{} {}'.format(first_name.lower(),
                                                  family_name.lower()):
                    found_users.append(user_file)
        # if len(found_users) == 0:
        #     raise UserNotFoundError(
        #             "No user found with the {} name in the repository!".format(name))
        # else:
        return found_users


    def find_users_by_email(self, email):
        all_files = UserManager.all_files_in_folder(self._location)
        found_users = []
        for user_file in all_files:
            with open(path.join(self._location, user_file)) as file_obj:
                for i, line in enumerate(file_obj):
                    if i + 1 == 4 and email.lower() in line.strip().lower():
                        found_users.append(user_file)
        # if len(found_users) == 0:
        #     raise UserNotFoundError(
        #             "No user found with the {} email in the repository!".format(email))
        # else:
        return found_users


    def find_users_by_role(self, role):
        role_manager = RoleManager(self.repository_location, self.paths_file)
        users_roles = role_manager.read_roles()
        found_users = []
        role = Role(role).role
        for id_key, roles_value in users_roles.iteritems():
            for role_obj in roles_value:
                if role == role_obj.role:
                    found_users.append(self.find_user_by_id(id_key))
        # if len(found_users) == 0:
        #     raise UserNotFoundError("No user found with the {} role in the repository!".format(role))
        # else:
        return found_users


    def add_role(self, user_id, role):
        role = Role(role)
        _ = self.find_user_by_id(user_id)
        role_manager = RoleManager(self.repository_location, self.paths_file)
        users_roles = role_manager.read_roles()
        if user_id not in users_roles:
            users_roles[user_id] = [role]
        else:
            if role not in users_roles[user_id]:
                users_roles[user_id].append(role)
        role_manager.write_roles(users_roles)


    def remove_role(self, user_id, role):
        role_manager = RoleManager(self.repository_location, self.paths_file)
        users_roles = role_manager.read_roles()
        _ = self.find_user_by_id(user_id)
        if user_id not in users_roles:
            raise RuntimeError(
                    "The user with {} user ID has no roles, can't remove {} role!".format(user_id, Role(role)))
        else:
            if Role(role) in users_roles[user_id]:
                users_roles[user_id] = users_roles[user_id].remove(Role(role))
            if not users_roles[user_id]:
                users_roles[user_id] = []
        role_manager.write_roles(users_roles)


    def has_role(self, user_id, role):
        role_manager = RoleManager(self.repository_location, self.paths_file)
        users_roles = role_manager.read_roles()
        if user_id not in users_roles:
            raise RuntimeError("No user with {} ID!".format(user_id))
        else:
            return Role(role) in users_roles[user_id]


    def list_users_by_role(self):
        role_manager = RoleManager(self.repository_location, self.paths_file)
        users_roles = role_manager.read_roles()
        users_by_roles = defaultdict(list)
        for id_key, roles_values in users_roles.iteritems():
            for role in roles_values:
                users_by_roles[role].append(id_key)
        return dict(users_by_roles)


    def check_role_file(self, roles_file=None):
        role_manager = RoleManager(self.repository_location, self.paths_file)
        user_roles = role_manager.read_roles()
        if not roles_file:
            roles_file = path.join(self._location, RoleManager.get_roles_file(self._location))
        if RoleManager.get_roles_file(self._location).endswith('txt'):
            with open(roles_file) as file_obj:
                user_ids = []
                for i, line in enumerate(file_obj):
                    if line.split(DELIMITER_CHAR)[0] == '':
                        raise ValueError("In the role file's {}th line has no user identifier!".format(i + 1))
                    elif DELIMITER_CHAR not in line or line.count(DELIMITER_CHAR) > 1:
                        raise ValueError(
                                "Missing or too many '{}' character in the {}th line!".format(DELIMITER_CHAR, i + 1))

                    roles = []
                    for role in line.split(DELIMITER_CHAR)[1].split(ROLE_DELIMITER_CHAR):
                        roles.append(role.strip())
                    roles_count = Counter(roles)
                    for key, value in roles_count.iteritems():
                        if value > 1:
                            raise ValueError("The {} role is duplicated in the {}th line!".format(key, i + 1))
                    for role in roles:
                        role = role.strip()
                        if role.isspace() or role == '':
                            raise ValueError(
                                    "Too many '{}' characters in the {}th line!".format(ROLE_DELIMITER_CHAR, i + 1))
                        Role(role)

                    user_ids.append(line.split(DELIMITER_CHAR)[0])
                user_ids_counter = Counter(user_ids)
                for key, value in user_ids_counter.iteritems():
                    if value > 1:
                        raise ValueError("The {} user id is duplicated!".format(key))
            return True


        elif RoleManager.get_roles_file(self._location).endswith('json'):
            with open(roles_file) as file_obj:
                data = load(file_obj)
            for id_key, roles_value in data.iteritems():
                if not isinstance(id_key, unicode):
                    raise MissingUserIdentifierError(
                            "In the role file has no user identifier!")
                else:
                    try:
                        int(id_key)
                    except ValueError:
                        MissingUserIdentifierError(
                                "In the role file the {} key should be a number!".format(
                                        id_key))
                if not isinstance(roles_value, list):
                    raise InvalidRoleNameError(
                            "The roles should be stored in a list, not in a {}!".format(
                                    type(roles_value).__name__))
                else:
                    for role in roles_value:
                        try:
                            Role(role)
                        except ValueError:
                            raise InvalidRoleNameError(
                                    "The {} role name is invalid!".format(role))
                    roles_count = Counter(roles_value)
                    for key, value in roles_count.iteritems():
                        if value > 1:
                            raise DuplicatedRolesError(
                                    "The {} role is duplicated!".format(key))
            return True

        elif RoleManager.get_roles_file(self._location).endswith('xml'):
            tree = ET.parse(roles_file)
            users_root = tree.getroot()
            users_list = []
            if users_root.tag != 'users':
                raise MissingUserIdentifierError(
                        "In the role file the root tag must be 'users' not {}!".format(
                                users_root.tag))
            for user in users_root:
                if user.tag != 'user':
                    raise MissingUserIdentifierError(
                            "In the role file the root's child tags must be 'user' not {}!".format(
                                    user.tag))
                try:
                    users_list.append(int(user.attrib['id']))
                except KeyError:
                    raise MissingUserIdentifierError("The user tag must have an 'id' attribute!")
                except ValueError:
                    raise MissingUserIdentifierError(
                            "The user tag must have an 'id' attribute which is a number, not a {}!".format(
                                    type(user.attrib['id']).__name__))
                user_roles = []
                for role in user:
                    try:
                        user_roles.append(Role(role.text))
                    except ValueError:
                        raise InvalidRoleNameError("The {} role name is invalid!".format(role))
                roles_count = Counter(user_roles)
                for key, value in roles_count.iteritems():
                    if value > 1:
                        raise DuplicatedRolesError("The {} role is duplicated!".format(key))
            users_list = Counter(user_roles)
            for key, value in users_list.iteritems():
                if value > 1:
                    raise DuplicatedRolesError("The {} user ID is duplicated!".format(key))
        else:
            raise WrongFileTypeError("The roles file's type is inappropriate it should be TXT, JSON or XML!")


    @classmethod
    def all_files_in_folder(cls, file_path, file_format=''):
        files_and_folders = listdir(file_path)
        all_files = []
        for item in files_and_folders:
            if path.isfile(path.join(file_path, item)) and item.split('.')[0] != 'roles':
                if len(file_format) != 0:
                    if item.endswith(file_format):
                        all_files.append(item)
                else:
                    all_files.append(item)
        return all_files


    def find_all_users(self):
        all_available_users = []
        for file_or_folder in listdir(self._location):
            if path.isfile(path.join(self._location, file_or_folder)):
                try:
                    all_available_users.append(int(file_or_folder))
                except:
                    pass
        return all_available_users


    def count_users(self):
        return len(self.find_all_users())


    def set_role_file(self, new_row_file_path):
        if path.exists(path.dirname(new_row_file_path)):
            role_file = path.join(self._location, RoleManager.get_roles_file(self._location))
            move(role_file, new_row_file_path)
            self._location = path.dirname(new_row_file_path)
        else:
            raise TypeError("The {} path doesn't exists!".format(path.dirnam(new_row_file_path)))
