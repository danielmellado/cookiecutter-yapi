import os
import pytest

from {{cookiecutter.package_name}} import {{cookiecutter.package_name}}


TESTDB_FILE = '/tmp/{{cookiecutter.package_name}}.db'
TEST_DATABASE_URI = 'sqlite:///' + TESTDB_FILE


@pytest.fixture
def database(request):
    {{cookiecutter.package_name}}.app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
    {{cookiecutter.package_name}}.app.config['TESTING'] = True
    with {{cookiecutter.package_name}}.app.app_context():
        {{cookiecutter.package_name}}.db.create_all()
        # pass

    def teardown():
        os.unlink(TESTDB_FILE)

    request.addfinalizer(teardown)


@pytest.fixture
def client(request):
    {{cookiecutter.package_name}}.app.config['TESTING'] = True
    client = {{cookiecutter.package_name}}.app.test_client()

    return client
