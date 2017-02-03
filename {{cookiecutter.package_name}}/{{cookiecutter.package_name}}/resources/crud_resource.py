"""
Crud Resources

This files defines two function intended to implement general
CRUD operation on a resource. These function are "templated"
class, that is; they returns a class which has been initialized
with the function arguments.

get_crud_resource returns a flask_restful Resource class with
the operation get, delete and put.

get_crud_list return a flask_restful Resource class with the
operation get (collection) and post
"""
import json
from pprint import pprint

from flask import request, jsonify, make_response, abort
from flask_restful import Resource


def get_crud_resource(db, Entity, get_schema, put_schema):

    class CrudResource(Resource):

        def get(self, id):
            object = Entity.query.get(id)
            if object is None:
                return abort(404)
            result = get_schema.dump(object)
            return jsonify(result.data)

        def delete(self, id):
            object = Entity.query.get(id)
            if object is None:
                return abort(404)
            db.session.delete(object)
            db.session.commit()
            return {"id": id}

        def put(self, id):
            object = Entity.query.get(id)
            if object is None:
                return abort(404)
            json_data = request.get_json(force=True)
            put_schema.context['object'] = object
            data, errors = put_schema.load(json_data)

            if any(errors):
                return make_response(jsonify(errors), 422)

            object.set(data)
            db.session.add(object)
            db.session.commit()

            return put_schema.dump(object)

    return CrudResource


def get_crud_list(db, Entity, get_collection_schema, post_schema):

    class CrudList(Resource):

        def query(self, args):
            if 'filters' in args:
                filters = json.loads(args['filters'])
                objects = Entity.query.filter_by(**filters)
            else:
                objects = Entity.query.all()

            return objects

        def get(self):
            # pprint(json.loads(request.args['filters']))
            objects = self.query(request.args)
            result = get_collection_schema.dump(objects)
            return jsonify(result.data)

        def post(self):
            json_data = request.get_json(force=True)
            data, errors = post_schema.load(json_data)

            if any(errors):
                return make_response(jsonify(errors), 422)

            object = Entity(data)
            db.session.add(object)
            db.session.commit()
            return make_response(jsonify(data), 201)

    return CrudList
