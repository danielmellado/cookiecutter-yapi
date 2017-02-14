"""
Crud Resources

This files defines two function intended to implement general
CRUD operation on a resource. These function are "templated"
class, that is; they returns a class which has been initialized
with the function arguments.

get_crud_resource returns a flask_restplus Resource class with
the operation get, delete and put.

get_crud_list return a flask_restplus Resource class with the
operation get (collection) and post
"""
import json
from pprint import pprint

from flask import request, jsonify, make_response, abort
from flask_restplus import Resource

from .. import api


def get_crud_resource(db, Entity, get_schema, put_schema, resource_fields):

    @api.doc(params={'id': 'The table identifier'})
    class CrudResource(Resource):

        @api.doc(responses={
            200: 'Success',
            404: 'Not Found'
        })
        def get(self, id):
            object = Entity.query.get(id)
            if object is None:
                return abort(404)
            result = get_schema.dump(object)
            return jsonify(result.data)

        @api.doc(responses={
            200: 'Success',
            404: 'Not Found'
        })
        def delete(self, id):
            object = Entity.query.get(id)
            if object is None:
                return abort(404)
            db.session.delete(object)
            db.session.commit()
            return {"id": id}

        @api.doc(
            body=resource_fields,
            responses={
                200: 'Success',
                404: 'Not Found',
                422: 'Unprocessable entity'
            }
        )
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


def get_crud_list(db, Entity, get_collection_schema, post_schema, resource_fields):

    class CrudList(Resource):

        def query(self, args):
            if 'filters' in args:
                filters = json.loads(args['filters'])
                objects = Entity.query.filter_by(**filters)
            else:
                objects = Entity.query.all()

            return objects

        @api.doc(responses={
            200: 'Success'
        })
        def get(self):
            # pprint(json.loads(request.args['filters']))
            objects = self.query(request.args)
            result = get_collection_schema.dump(objects)
            return jsonify(result.data)

        @api.doc(
            body=resource_fields,
            responses={
                201: 'Created',
                422: 'Unprocessable entity'
            }
        )
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
