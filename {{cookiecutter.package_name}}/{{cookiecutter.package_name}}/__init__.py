from .{{cookiecutter.package_name}} import app, db, ma, api
from .end_points import create_endpoints
from .commands import *
from .model import *


create_endpoints()
