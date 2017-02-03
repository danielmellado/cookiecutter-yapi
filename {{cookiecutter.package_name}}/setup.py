from setuptools import setup

setup(
    name='{{cookiecutter.package_name}}',
    packages=['{{cookiecutter.package_name}}', '{{cookiecutter.package_name}}.resources'],
    version='{{cookiecutter.package_version}}',
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-restful',
        'flask-sqlalchemy',
        'flask-migrate',
        'flask-marshmallow',
        'mysqlclient'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
