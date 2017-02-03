import json
import pytest

from {{cookiecutter.package_name}} import {{cookiecutter.package_name}}
from {{cookiecutter.package_name}}.model import PDN
from bootstrap import *


@pytest.fixture
def add_pdn(request):
    {{cookiecutter.package_name}}.app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
    {{cookiecutter.package_name}}.app.config['TESTING'] = True
    with {{cookiecutter.package_name}}.app.app_context():
        pdn = PDN({'codigo': 'pdn_prueba', 'descripcion': 'pdn de prueba'})
        {{cookiecutter.package_name}}.db.session.add(pdn)
        {{cookiecutter.package_name}}.db.session.commit()


@pytest.fixture
def add_two_pdns(request):
    {{cookiecutter.package_name}}.app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
    {{cookiecutter.package_name}}.app.config['TESTING'] = True
    with {{cookiecutter.package_name}}.app.app_context():
        pdn = PDN({'codigo': 'pdn_prueba', 'descripcion': 'pdn de prueba'})
        pdn2 = PDN({'codigo': 'pdn_prueba2', 'descripcion': 'pdn2 de prueba'})
        {{cookiecutter.package_name}}.db.session.add(pdn)
        {{cookiecutter.package_name}}.db.session.add(pdn2)
        {{cookiecutter.package_name}}.db.session.commit()


@pytest.fixture
def add_three_pdns(request):
    {{cookiecutter.package_name}}.app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
    {{cookiecutter.package_name}}.app.config['TESTING'] = True
    with {{cookiecutter.package_name}}.app.app_context():
        pdn = PDN({'codigo': 'pdn_prueba', 'descripcion': 'pdn de prueba'})
        pdn2 = PDN({'codigo': 'pdn_prueba2', 'descripcion': 'pdn2 de prueba'})
        pdn3 = PDN({'codigo': 'pdn_prueba3', 'descripcion': 'pdn de prueba'})
        {{cookiecutter.package_name}}.db.session.add(pdn)
        {{cookiecutter.package_name}}.db.session.add(pdn2)
        {{cookiecutter.package_name}}.db.session.add(pdn3)
        {{cookiecutter.package_name}}.db.session.commit()


def test_foo(client):
    """Start with a blank database."""
    rv = client.get('/foo')
    assert b'hola' in rv.data


def test_create_pdn(client, database):
    """ Creates a pdn """
    rv = client.post('/pdn',
                     data=json.dumps({'codigo': 'pdn_prueba',
                                      'descripcion': 'pdn de pruebas',
                                      'ip_master': '10.10.10.10'}))
    assert u'201' in rv.status
    assert b'"codigo": "pdn_prueba"' in rv.data


def test_delete_pdn(client, database, add_pdn):
    """ Deletes a pdn """
    rv = client.delete('/pdn/1')
    pdns = {{cookiecutter.package_name}}.db.session.query(PDN).all()

    assert u'200' in rv.status
    assert len(pdns) == 0


def test_get_pdn(client, database, add_pdn):
    rv = client.get('/pdn/1')

    assert u'200' in rv.status
    assert b'"codigo": "pdn_prueba"' in rv.data


def test_get_all_pdns(client, database, add_two_pdns):
    rv = client.get('/pdn')

    pdns = json.loads(rv.data.decode('utf8'))

    assert u'200' in rv.status
    assert len(pdns) == 2


def test_filter_pdns(client, database, add_three_pdns):
    rv = client.get('/pdn?filters={"descripcion":"pdn de prueba"}')

    pdns = json.loads(rv.data.decode('utf8'))

    assert u'200' in rv.status
    assert len(pdns) == 2


def test_create_duplicate_pdn(client, database, add_pdn):
    rv = client.post('/pdn',
                     data=json.dumps({'codigo': 'pdn_prueba',
                                      'descripcion': 'pdn de pruebas',
                                      'ip_master': '10.10.10.10'}))
    assert u'422' in rv.status


def test_create_pdn_without_codigo(client, database):
    rv = client.post('/pdn',
                     data=json.dumps({'descripcion': 'pdn de pruebas',
                                      'ip_master': '10.10.10.10'}))
    assert u'422' in rv.status


def test_change_pdn(client, database, add_pdn):
    rv = client.put('/pdn/1',
                    data=json.dumps({'codigo': 'pdn_prueba',
                                     'descripcion': 'pdn de pruebas cambio',
                                     'ip_master': '10.10.10.20'}))

    assert u'200' in rv.status
    assert b'cambio' in rv.data
    assert b'10.10.10.20' in rv.data


def test_change_pdn_bad_ip(client, database, add_pdn):
    rv = client.put('/pdn/1',
                    data=json.dumps({'codigo': 'pdn_prueba',
                                     'descripcion': 'pdn de pruebas cambio',
                                     'ip_master': '10.10.10.560'}))

    assert u'422' in rv.status
