#!/usr/bin/env python
"""This file contains the implementation of :py:class:Project class.

The :py:class:Project is represented of name, description, :py:class:Document and :py:class:User (members) objects.
"""

# Imports -----------------------------------------------------------------------------------------------------------
from os import path, makedirs, listdir
from shutil import rmtree

from iniformat.reader import read_ini_file
from iniformat.writer import write_ini_file
from storage_utils import get_next_id

# Authorship information  -------------------------------------------------------------------------------------------
__author__ = "Zsolt Bokor Levente"
__copyright__ = "Copyright 2016, Morgan Stanely - Training 360 Project"
__credits__ = "Zsolt Bokor Levente"
__version__ = "1.0.0"
__maintainer__ = "Zsolt Bokor Levente"
__email__ = ["bokor.zsolt5@gmail.com", "bokorzsolt@yahoo.com"]
__status__ = "Development"

# -------------------------------------------------------------------------------------------------------------------

PROJECT_METADATA_FILE_NAME_FORMAT = '{}_project_metadata.edd'

class Project(object):
    """
    The :py:class:Project class of the :py:class:Repository.

    It has name, description, members (:py:class:User list) and documents (:py:class:Document list).
    """

    def __init__(self, name, description, members = None, documents = None):
        """
        Initialisation of a new :py:class:Project object.

        :param name: Name of the :py:class:Project.
        :param description: Description of the :py:class:Project.
        :param members: The author(s) (:py:class:User) of the :py:class:Project. If only one member is passed the
        :py:attr:_members is converted to list.
        :param documents: The document(s) (:py:class:Document) of the :py:class:Project. If only one document is passed
        the :py:attr:_documents is converted to list.
        """
        self._name = name
        self._description = description
        if not members:
            self._members = []
        else:
            self._members = members
        if not documents:
            self._documents = []
        else:
            self._documents = documents

    @property
    def name(self):
        """
        The property of the :py:attr:_name attribute.

        :return: The title of the :py:class:Project object :py:attr:_name.
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        The setter of the :py:attr:_name.

        :param value: New name.
        :return:
        """
        raise AttributeError("The name of a project can't be changed!")

    @property
    def description(self):
        """
        The property of the :py:attr:_description attribute.

        :return: The title of the :py:class:Project object :py:attr:_description.
        """
        return self._description

    @description.setter
    def description(self, value):
        """
        The setter of the :py:attr:_description.

        :param value: New description.
        :return:
        """
        self._description = value

    @property
    def members(self):
        """
        The property of the :py:attr:_members attribute.

        :return: The title of the :py:class:Project object :py:attr:_members.
        """
        return self._members

    @members.setter
    def members(self, value):
        """
        The setter of the :py:attr:_members. The :py:attr:members can't be changed like this only with the
        :py:meth:add_member and :py:meth:remove_member method.

        :param value: New members.
        :exception AttributeError is raised every time the :py:attr:members is changed.
        :return:
        """
        raise AttributeError(
            "The members of a project can't be changed like this, use the add_member or remove_member methods!")

    @property
    def documents(self):
        """
        The property of the :py:attr:_documents attribute.

        :return: The title of the :py:class:Project object :py:attr:_documents.
        """
        return self._documents

    @documents.setter
    def documents(self, value):
        """
        The setter of the :py:attr:_documents. The :py:attr:documents can't be changed like this only with the
        :py:meth:add_document and :py:meth:remove_document method.

        :param value: New documents.
        :exception AttributeError is raised every time the :py:attr:documents is changed.
        :return:
        """
        raise AttributeError(
            "The documents of a project can't be changed like this, use the add_document or remove_document methods!")

    def add_member(self, user_id):
        """
        Adds a :py:class:User object's ID to the :py:attr:members (list).

        :param user_id: ID of a new :py:class:User object.
        :exception AttributeError is raised if the ``user_id`` is not an instance of integer.
        :return:
        """
        if isinstance(user_id, int):
            self._members.append(user_id)
        else:
            raise AttributeError("The user_id must be a number!")

    def remove_member(self, user_id):
        """
        Removes a :py:class:User object's ID to the :py:attr:members (list).

        :param user_id: ID of a new :py:class:User object.
        :exception AttributeError is raised if the ``user_id`` is not an instance of integer.
        :return:
        """
        if isinstance(user_id, int):
            try:
                self._members.remove(user_id)
            except ValueError:
                pass
        else:
            AttributeError("The user_id must be a number!")

    def add_document(self, document_id):
        """
        Adds a :py:class:Document object's ID to the :py:attr:documents (list).

        :param document_id: ID of a new :py:class:Document object.
        :exception AttributeError is raised if the ``document_id`` is not an instance of integer.
        :return:
        """
        if isinstance(document_id, int):
            self._documents.append(document_id)
        else:
            raise AttributeError("The document_id must be a number!")

    def remove_document(self, document_id):
        """
        Removes a :py:class:Document object's ID to the :py:attr:_documents (list).

        :param document_id: ID of a new :py:class:Document object.
        :exception AttributeError is raised if the ``document_id`` is not an instance of integer.
        :return:
        """
        if isinstance(document_id, int):
            try:
                self._documents.remove(document_id)
            except ValueError:
                pass
        else:
            AttributeError("The document_id must be a number!")

    def has_required_roles(self, repository):
        users_by_role = repository._user_manager.list_users_by_role()
        administrators = users_by_role['admin']
        managers = users_by_role['manager']
        is_adminstrator = False
        is_manager = False
        for user_id in self.members:
            if user_id in administrators:
                is_adminstrator = True
                break

        for user_idin in self.members:
            if user_id in managers:
                is_manager = False
                break
        return is_adminstrator and is_manager


class ProjectManager(object):
    def __init__(self, project_path, user_manager):
        self._location = project_path
        self._user_manager = user_manager
        self._projects = []
        self.load()

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        raise AttributeError("The location of a project can't be changed!")

    @property
    def user_manager(self):
        return self._user_manager

    @user_manager.setter
    def user_manager(self, value):
        raise AttributeError("The user manager of a project can't be changed!")

    def load(self):
        """Try to load an existing repository"""
        if path.exists(self._location):
            if not path.isdir(self._location):
                raise ValueError('The repository should be a directory!')
            self._projects = self.load_projects_ids()
        else:
            self.initialize()

    def initialize(self):
        """Initialize a new repository"""
        makedirs(self._location)

    def load_projects_ids(self):
        projects = []
        for file_or_folder in listdir(self.location):
            if path.isdir(file_or_folder):
                try:
                    projects.append(int(file_or_folder))
                except:
                    pass
        return projects

    def count_projects(self):
        return len(self._projects)

    def save_project(self, project, next_id):
        data = {
            'project': {
                'name': project.name,
                'description': project.description,
                'members': str(project.members),
                'documents': str(project.documents)
            }
        }
        project_path = path.join(self.location, str(next_id))
        project_metadata_path = path.join(project_path, PROJECT_METADATA_FILE_NAME_FORMAT.format(next_id))
        if not path.exists(project_path):
            makedirs(project_path)
        write_ini_file(project_metadata_path, data)
        return next_id


    def add_project(self, project):
        new_project_id = self.save_project(project, get_next_id(self.location))
        self._projects.append(new_project_id)
        return new_project_id

    def load_project(self, project_id):
        project_path = path.join(self.location, str(project_id))
        if path.exists(project_path):
            project_metadata_path = path.join(project_path, PROJECT_METADATA_FILE_NAME_FORMAT.format(project_id))
            project_data = read_ini_file(project_metadata_path)['project']
            return Project(project_data['name'], project_data['description'], project_data['members'],
                           project_data['documents'])
        else:
            raise ValueError("The {} path doesn't exists!".format(project_path))

    def find_project_by_id(self, project_id):
        try:
            return self.load_project(project_id)
        except ValueError:
            raise ValueError("The project with {} ID doesn't exists!".format(project_id))

    def find_projects_by_name(self, name):
        found_projects = []
        for project_id in self._projects:
            project = self.find_project_by_id(project_id)
            if name.lower() in project.name.lower():
                found_projects.append(project)
        return found_projects

    def update_project(self, project_id, project):
        if project_id in self._projects:
            self.save_project(project, project_id)
        else:
            raise ValueError("The project with {} ID doesn't exists, it can't be updated!".format(project_id))

    def delet_project_in_file_system(self, project_id):
        rmtree(path.join(self.location, str(project_id)))

    def remove_project(self, project_id):
        if project_id in self._projects:
            self._projects.remove(project_id)
            self.delet_project_in_file_system(project_id)
        else:
            raise ValueError("The project with {} ID doesn't exists, it can't be removed!".format(project_id))
