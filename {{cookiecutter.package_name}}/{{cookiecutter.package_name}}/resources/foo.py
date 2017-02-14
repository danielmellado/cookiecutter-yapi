from flask_restplus import Resource


class Foo(Resource):
    def get(self):
        return {'hola': 'foo'}
