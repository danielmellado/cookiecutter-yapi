from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from .config import default


app = Flask(__name__)
api = Api(
    app,
    version='{{cookiecutter.package_version}}',
    default='',
    default_label='',
    title="{{cookiecutter.package_name}}",
    description="{{cookiecutter.package_name}} description"
)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

app.config.update(default)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)
