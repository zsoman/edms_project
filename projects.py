from os import path, makedirs, listdir

class Project(object):
    def __init__(self, name, description, members = [], documents = []):
        self._name = name
        self._description = description
        self._members = members
        self._documents = documents

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("The name of a project can't be changed!")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def members(self):
        return self._members

    @members.setter
    def members(self, value):
        raise AttributeError(
            "The members of a project can't be changed like this, use the add_member or remove_member methods!")

    @property
    def documents(self):
        return self._documents

    @documents.setter
    def documents(self, value):
        raise AttributeError(
            "The documents of a project can't be changed like this, use the add_document or remove_document methods!")

    def add_member(self, user):
        self._members.append(user)

    def remove_member(self, user):
        self._members.remove(user)

    def add_document(self, document):
        self._documents.append(document)

    def remove_document(self, document):
        self._members.remove(document)

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
            self._projects = self.load_projects()
        else:
            self.initialize()

    def initialize(self):
        """Initialize a new repository"""
        makedirs(self._location)

    def load_projects(self):
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

    def add_project(self, project):
        pass
        # TODO

    def find_project_by_id(self, a_id):
        pass
        # TODO

    def update_project(self, project_id, b):
        pass
        # TODO

    def remove_project(self, a_id):
        pass
        # TODO

    def find_projects_by_name(self, param):
        pass
        # TODO
