from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from .config import default


app = Flask(__name__, instance_relative_config=True)
api = Api(app,version='{{cookiecutter.package_version}}', doc='/doc', default="API", default_label="{{cookiecutter.package_name}}")
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

app.config.update(default)
app.config.from_pyfile('config.py')
app.config.from_envvar('APP_CONFIG_FILE')


@app.route('/')
def home():
    return app.config['PARAM2']
