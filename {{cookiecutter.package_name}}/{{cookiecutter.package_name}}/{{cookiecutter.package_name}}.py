from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from .config import default


app = Flask(__name__, instance_relative_config=True)
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

app.config.update(default)
app.config.from_pyfile('config.py')
app.config.from_envvar('APP_CONFIG_FILE')


@app.route('/')
def home():
    return app.config['PARAM2']
