from flask_restplus import Resource
from .. import app


class Foo(Resource):
    def get(self):
        return {'hola': app.config['PARAM1']}
