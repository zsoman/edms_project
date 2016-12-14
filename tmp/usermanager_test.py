from os import path

from repository import Repository
from usergen.generator import UserGenerator
from users import User, UserManager, RoleManager, Role

admin_role = Role('admin')
manager_role = Role('manager')
author_role = Role('author')
reviewer_role = Role('reviewer')
visitor_role = Role('visitor')

repo = Repository()
gen = UserGenerator()
fname = gen.generate_first_name()
lname = gen.generate_family_name()
birth = gen.generate_birth_date()
email = gen.generate_email(fname, lname)
password = gen.generate_password()
user = User(fname, lname, birth, email, password)

user_manager = UserManager(path.join(repo._location, 'users'))
user_manager.save_user('1', user)
print(user_manager.find_users_by_name('{} {}'.format(fname, lname)))
print(user_manager.find_users_by_email(email))
print(user_manager.find_users_by_role(author_role))
print(user_manager.find_users_by_role(admin_role))
role_manager = RoleManager(path.join(repo._location, 'users'))
print(role_manager.read_roles())
role_manager.write_roles({999: [author_role, visitor_role], 998: [reviewer_role]})
print(role_manager.read_roles())
