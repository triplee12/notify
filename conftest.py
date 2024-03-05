import pytest
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import create_app
from models import orm
from views import service_blueprint



@pytest.fixture
def application():
    app = create_app('test_config')
    with app.app_context():
        orm.create_all()
        yield app
        orm.session.remove()
        orm.drop_all()


@pytest.fixture
def client(application):
    return application.test_client()
