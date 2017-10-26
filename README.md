Cookiecutter-yapi
=================

This templates generates a Flask project with the following
extensions:

- Flask-SQLAlchemy for the model and database management
- Flask-Restful for api resource based on Resource classes
- Flask-Migrate for database migration
- Flask-Marshmallow for request validation an JSON dumping
- pytest

The API is architectured like a python package ready to be
installed with pip and packaged with wheel. The code organization
has been taken from

    http://flask.pocoo.org/docs/0.12/tutorial/packaging

In order to create a REST API from this cookiecutter install
cookiecutter:

    pip install cookiecutter

and generates the API:

    cookiecutter https://github.com/juanda/cookiecutter-yapi

Follow the instructions given in the README.rst file of the project
and take a look at the code to understand it and feel confortable
with it.

And that's all folks!

Note: Only tested in python 3
