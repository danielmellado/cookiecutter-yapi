from .{{cookiecutter.package_name}} import app, db, ma
from .end_points import create_endpoints
from .commands import *
from .model import *


create_endpoints()
