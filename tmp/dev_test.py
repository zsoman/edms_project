from os import path

from repository import Repository
from usergen.generator import UserGenerator
from users import User, UserManager, RoleManager, Role

admin_role = Role('admin')
manager_role = Role('manager')
author_role = Role('author')
reviewer_role = Role('reviewer')
visitor_role = Role('visitor')

repo = Repository(location='./tmp/edms/users', roles_file_type='json')
gen = UserGenerator()
fname = gen.generate_first_name()
lname = gen.generate_family_name()
birth = gen.generate_birth_date()
email = gen.generate_email(fname, lname)
password = gen.generate_password()
user = User(fname, lname, birth, email, password)

user_manager = UserManager(path.join(repo._location, 'users'))
user_manager.save_user('1', user)

user_manager.add_role_to_user(999, author_role)
user_manager.add_role_to_user(999, manager_role)
user_manager.add_role_to_user(998, manager_role)
user_manager.add_role_to_user(997, visitor_role)
user_manager.add_role_to_user(997, reviewer_role)
user_manager.add_role_to_user(997, admin_role)

print(user_manager.find_users_by_name('{} {}'.format(fname.upper(), lname)))
print(user_manager.find_users_by_email(email.upper()[:7]))
print(user_manager.find_users_by_role(author_role))
print(user_manager.find_users_by_role(admin_role))
role_manager = RoleManager(path.join(repo._location, 'users'))
print(role_manager.read_roles())
role_manager.write_roles({999: [author_role, visitor_role], 998: [reviewer_role]})
print(role_manager.read_roles())

user_manager.add_role_to_user(999, admin_role)
user_manager.add_role_to_user(997, admin_role)
user_manager.remove_role_from_user(998, reviewer_role)

user_manager.user_has_specific_role(999, admin_role)
user_manager.user_has_specific_role(998, reviewer_role)
# user_manager.user_has_specific_role(996, reviewer_role)

for key, value in user_manager.list_users_by_role().iteritems():
    print("{}: {}".format(key, value))

print(user_manager.check_role_file())
