import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:yourPassword@127.0.0.1/notify'
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')

# Pagination configuration
PAGINATION_PAGE_SIZE = 4
PAGINATION_PAGE_ARGUMENT_NAME = 'page'
