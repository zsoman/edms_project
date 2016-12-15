from os import path, makedirs

from docgen.generator import DocumentGenerator
from documents import DocumentManager, Document
from iniformat.reader import read_ini_file
from repository import Repository
from usergen.generator import UserGenerator
from users import User, UserManager, RoleManager, Role


# Role creation
admin_role = Role('admin')
manager_role = Role('manager')
author_role = Role('author')
reviewer_role = Role('reviewer')
visitor_role = Role('visitor')

repo = Repository(roles_file_type='json')  # Create repo
gen = UserGenerator()  # Create user_gerenerator

# Generate user data
fname = gen.generate_first_name()
lname = gen.generate_family_name()
birth = gen.generate_birth_date()
email = gen.generate_email(fname, lname)
password = gen.generate_password()

# Create user from generated data
user = User(fname, lname, birth, email, password)

# Create user_manager
user_manager = UserManager(repo)

# User manipulation
user_manager.save_user('1', user)

user_manager.add_role_to_user(999, author_role)
user_manager.add_role_to_user(999, manager_role)
user_manager.add_role_to_user(998, manager_role)
user_manager.add_role_to_user(997, visitor_role)
user_manager.add_role_to_user(997, reviewer_role)
user_manager.add_role_to_user(997, admin_role)

# Search users by
print("\n## Search for users by ##")
print(user_manager.find_users_by_name('{} {}'.format(fname.upper(), lname)))
print(user_manager.find_users_by_email(email.upper()[:7]))
print(user_manager.find_users_by_role(author_role))
print(user_manager.find_users_by_role(admin_role))

# Create role_manager
role_manager = RoleManager(repo)

# Role_manager usage
print("\n## Role manager usage ##")
print(role_manager.read_roles())
role_manager.write_roles({999: [author_role, visitor_role], 998: [reviewer_role]})
print(role_manager.read_roles())

user_manager.add_role_to_user(999, admin_role)
user_manager.add_role_to_user(997, admin_role)
user_manager.remove_role_from_user(998, reviewer_role)

user_manager.user_has_specific_role(999, admin_role)
user_manager.user_has_specific_role(998, reviewer_role)
# user_manager.user_has_specific_role(996, reviewer_role)

print("\n## List users by role ##")
for key, value in user_manager.list_users_by_role().iteritems():
    print("{}: {}".format(key, value))

print("\n## Check role file ##")
print(user_manager.check_role_file())

# Create document_manager
doc_manager = DocumentManager(repo)

# Create document_gerator
doc_generator = DocumentGenerator()
if not path.exists('Documents'):
    makedirs('Documents')
metadata1 = doc_generator.generate_metadata('office')
metadata2 = doc_generator.generate_metadata('general')
path_file1 = path.join('Documents', metadata1['filename'])
path_file2 = path.join('Documents', metadata2['filename'])
doc_generator.generate_random_file(path_file1)
doc_generator.generate_random_file(path_file2)

# Create document
document = Document(metadata1['title'], metadata1['description'], [999, 998], [path_file1, path_file2], 'txt')

doc_manager.add_document(document)
print(read_ini_file('Repositories/repo_1/documents/1/1_document_metadata.ini'))

# Test the document load by adding it again with new files to the repository
loaded_doc = doc_manager.load_document(1)

metadata3 = doc_generator.generate_metadata('office')
metadata4 = doc_generator.generate_metadata('general')
path_file3 = path.join('Documents', metadata3['filename'])
path_file4 = path.join('Documents', metadata4['filename'])
doc_generator.generate_random_file(path_file3)
doc_generator.generate_random_file(path_file4)

loaded_doc.files = [path_file3, path_file4]
doc_manager.add_document(loaded_doc)

# Test the document update
metadata5 = doc_generator.generate_metadata('office')
path_file5 = path.join('Documents', metadata5['filename'])
doc_generator.generate_random_file(path_file5)

update_document = Document(metadata5['title'], metadata5['description'], [999, 998], [path_file5], 'txt')
doc_manager.update_document(1, update_document)
print(read_ini_file('Repositories/repo_1/documents/1/1_document_metadata.ini'))

# Remove docuement from file system
# doc_manager.remove_document(2)

# Find all availabal documents id
print(doc_manager.find_all_documents())

# Load all docuements
for doc_id_key, doc_value in doc_manager.load_all_documents().iteritems():
    print("{}: {}".format(doc_id_key, doc_value))

# Find document by
print("\nFound document by id:")
print(doc_manager.find_document_by_id(1))
print("\nFound documents by title:")
for doc_id_key, doc_value in doc_manager.find_document_by_title(metadata5['title']).iteritems():
    print("{}: {}".format(doc_id_key, doc_value))
print("\nFound documents by author:")
for doc_id_key, doc_value in doc_manager.find_document_by_author(999).iteritems():
    print("{}: {}".format(doc_id_key, doc_value))
print("\nFound documents by format:")
for doc_id_key, doc_value in doc_manager.find_document_by_format('txt').iteritems():
    print("{}: {}".format(doc_id_key, doc_value))

# Existence of document files
# remove('Repositories/repo_1/documents/1/{}'.format(metadata5['filename']))
print(doc_manager.document_files_exist(1))
print(doc_manager.unreferenced_document_files(1))
doc_manager.remove_document_files(1)
