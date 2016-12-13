from os import path

from repository import Repository
from usergen.generator import UserGenerator
from users import User, UserManager

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
print(user_manager.find_users_by_role('author'))
print(user_manager.find_users_by_role('admin'))
