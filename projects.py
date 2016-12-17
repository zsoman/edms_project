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
