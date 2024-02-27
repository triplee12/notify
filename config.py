import os

BASE_DIR = os.path.join(os.path.dirname(__file__)),
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'postgresql://myPassword:postgres/notify'
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
