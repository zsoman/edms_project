from os import path, makedirs
from random import choice

from docgen.new_generator import NewDocumentGenerator, DocumentGenerator
from documents import Document
from repository import Repository
from usergen.generator import UserGenerator
from users import User

# Role creation
# admin_role = Role('admin')
# manager_role = Role('manager')
# author_role = Role('author')
# reviewer_role = Role('reviewer')
# visitor_role = Role('visitor')

repo = Repository()  # Create repo
gen = UserGenerator()  # Create user_gerenerator
# # # Create user_manager
# # user_manager = UserManager(repo)
# # # Create document_manager
# # doc_manager = DocumentManager(repo)
# #
# # repo.add_user_manager(user_manager)
# # repo.add_document_manager(doc_manager)
#
# # Generate user data
# fname = gen.generate_first_name()
# lname = gen.generate_family_name()
# birth = gen.generate_birth_date()
# email = gen.generate_email(fname, lname)
# password = gen.generate_password()
# #
# # # Create user from generated data
# user = User(fname, lname, birth, email, password)
# user = User(fname + '2', lname + '2', birth, email, password)
#
# # User manipulation
# repo._user_manager.save_user('1', user)
# repo._user_manager.save_user('2', user)
#
# repo._user_manager.add_role(1, 'author')
# repo._user_manager.add_role(1, 'manager')
# repo._user_manager.add_role(2, 'manager')
# repo._user_manager.add_role(2, 'visitor')
# repo._user_manager.add_role(2, 'reviewer')
# repo._user_manager.add_role(2, 'admin')
#
# # Search users by
# print("\n## Search for users by ##")
# print(repo._user_manager.find_users_by_name('{} {}'.format(fname.upper(), lname)))
# print(repo._user_manager.find_users_by_email(email.upper()[:7]))
# print(repo._user_manager.find_users_by_role('author'))
# print(repo._user_manager.find_users_by_role('admin'))
#
# # Create role_manager
# # role_manager = RoleManager(repo._location, repo._paths_file)
#
# # Role_manager usage
# # print("\n## Role manager usage ##")
# # print(role_manager.read_roles())
# # role_manager.write_roles({1: ['author', 'visitor'], 2: ['reviewer', 'admin']})
# # print(role_manager.read_roles())
#
# repo._user_manager.add_role(1, 'admin')
# repo._user_manager.add_role(2, 'admin')
# repo._user_manager.remove_role(2, 'reviewer')
#
# repo._user_manager.has_role(1, 'admin')
# repo._user_manager.has_role(2, 'reviewer')
# # repo._user_manager.has_role(996, 'reviewer')
#
# print("\n## List users by role ##")
# for key, value in repo._user_manager.list_users_by_role().iteritems():
#     print("{}: {}".format(key, value))
#
# print("\n## Check role file ##")
# # print(repo._user_manager.check_role_file())
#
#
# # Create document_gerator
#
# doc_generator = DocumentGenerator()
# if not path.exists('Documents'):
#     makedirs('Documents')
#
# metadata1 = doc_generator.generate_metadata(choice(['general', 'office', 'image']))
# metadata2 = doc_generator.generate_metadata('general')
# path_file1 = path.join('Documents', metadata1['filename'])
# path_file2 = path.join('Documents', metadata2['filename'])
# doc_generator.generate_random_file(path_file1)
# doc_generator.generate_random_file(path_file2)
#
# # Create document
# document = Document(metadata1['title'], metadata1['description'], [1, 2], [path_file1, path_file2], 'txt')
#
# repo._document_manager.add_document(document)
#
# # print(read_ini_file('Repositories/repo_1/documents/1/1_document_metadata.edd'))
#
# # Test the document load by adding it again with new files to the repository
# loaded_doc = repo._document_manager.load_document(1)
#
# metadata3 = doc_generator.generate_metadata('office')
# metadata4 = doc_generator.generate_metadata('general')
# path_file3 = path.join('Documents', metadata3['filename'])
# path_file4 = path.join('Documents', metadata4['filename'])
# doc_generator.generate_random_file(path_file3)
# doc_generator.generate_random_file(path_file4)
#
# loaded_doc.files = [path_file3, path_file4]
# repo._document_manager.add_document(loaded_doc)
#
# # Test the document update
# metadata5 = doc_generator.generate_metadata('office')
# path_file5 = path.join('Documents', metadata5['filename'])
# doc_generator.generate_random_file(path_file5)
#
# update_document = Document(metadata5['title'], metadata5['description'], [1, 2], [path_file5], 'txt')
# repo._document_manager.update_document(1, update_document)
# # print(read_ini_file('Repositories/repo_1/documents/1/1_document_metadata.edd'))
#
# # Remove docuement from file system
# # repo._document_manager.remove_document(2)
#
# # Find all availabal documents id
# print(repo._document_manager.find_all_documents())
#
# # Load all docuements
# # for doc_id_key, doc_value in repo._document_manager.load_all_documents().iteritems():
# #     print("{}: {}".format(doc_id_key, doc_value))
#
# # Find document by
# print("\nFound document by id:")
# # print(repo._document_manager.find_document_by_id(1))
# print("\nFound documents by title:")
# # for doc_id_key, doc_value in repo._document_manager.find_documents_by_title(metadata5['title']):
# #     print("{}: {}".format(doc_id_key, doc_value))
# print("\nFound documents by author:")
# # for doc_id_key, doc_value in repo._document_manager.find_documents_by_author(1):
# #     print("{}: {}".format(doc_id_key, doc_value))
# print("\nFound documents by format:")
# # for doc_id_key, doc_value in repo._document_manager.find_documents_by_format('txt'):
# #     print("{}: {}".format(doc_id_key, doc_value))
#
# # Existence of document files
# # remove('Repositories/repo_1/documents/1/{}'.format(metadata5['filename']))
# # print(repo._document_manager.document_files_exist(1))
# # print(repo._document_manager.unreferenced_document_files(1))
# # repo._document_manager.remove_document_files(1)

# Test the new document generator
new_doc_gen = NewDocumentGenerator('Documents', repo._user_manager, repo._document_manager)
# new_doc_gen = NewDocumentGenerator('/tmp/samples/importable', repo._user_manager, repo._document_manager)
new_doc_gen.generate_many_documents(2)
repo.import_documents('Documents')

fname = gen.generate_first_name()
lname = gen.generate_family_name()
birth = gen.generate_birth_date()
email = gen.generate_email(fname, lname)
password = gen.generate_password()
#
# # Create user from generated data
user = User(fname, lname, birth, email, password)
user = User(fname + '2', lname + '2', birth, email, password)

# User manipulation
repo._user_manager.save_user('1', user)
repo._user_manager.save_user('2', user)

repo._user_manager.add_role(1, 'author')
repo._user_manager.add_role(1, 'manager')
repo._user_manager.add_role(2, 'manager')
repo._user_manager.add_role(2, 'visitor')

repo.create_backup(verbose = True, backup_projects = False, backup_users = False)

doc_generator = DocumentGenerator()
if not path.exists('Documents'):
    makedirs('Documents')

metadata1 = doc_generator.generate_metadata(choice(['general', 'office', 'image']))
metadata2 = doc_generator.generate_metadata('general')
path_file1 = path.join('Documents', metadata1['filename'])
path_file2 = path.join('Documents', metadata2['filename'])
doc_generator.generate_random_file(path_file1)
doc_generator.generate_random_file(path_file2)

# Create document
document = Document(metadata1['title'], metadata1['description'], [1, 2], [path_file1, path_file2], 'txt')

repo._document_manager.add_document(document)

repo.restore(verbose = True, backup_documents = False)

# repo.retrieve_info_of_repository()
# repo.show_repository_info()



# repo._document_manager.remove_document(1)
# repo._document_manager.remove_document(2)

# repo.import_documents('Repositories/repo_1/sample')
