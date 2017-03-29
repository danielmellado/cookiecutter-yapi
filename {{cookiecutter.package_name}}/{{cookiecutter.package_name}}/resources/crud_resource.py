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

from .. import  api

def get_crud_resource(db, Entity, get_schema, put_schema, resource_fields=None):

    @api.doc(params={'id': 'The table identifier'})
    class CrudResource(Resource):

        @api.doc(responses={
            200: 'Success',
            404: 'Not Found'
        })
        def get(self, id):
            obj = Entity.query.get(id)
            if obj is None:
                return abort(404)
            result = get_schema.dump(obj)
            return jsonify(result.data)

        @api.doc(responses={
            200: 'Success',
            404: 'Not Found'
        })
        def delete(self, id):
            obj = Entity.query.get(id)
            self.pre_delete(obj)
            if obj is None:
                return abort(404)
            db.session.delete(obj)
            db.session.commit()
            # No hacemos post delete pues después de borrar no se debería hacer nada
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
            obj = Entity.query.get(id)
            self.pre_update(obj)
            if obj is None:
                return abort(404)
            json_data = request.get_json(force=True)
            put_schema.context['obj'] = obj
            data, errors = put_schema.load(json_data)

            if any(errors):
                return make_response(jsonify(errors), 422)

            obj.set(data)
            db.session.add(obj)
            db.session.commit()
            self.post_update(obj)

            return put_schema.dump(obj)

        def pre_update(self, obj):
            pass

        def post_update(self, obj):
            pass

        def pre_delete(self, obj):
            pass


    return CrudResource


def get_crud_list(db, Entity, get_collection_schema, post_schema, resource_fields=None):

    class CrudList(Resource):

        def _query(self, args):
            if 'filters' in args:
                filters = json.loads(args['filters'])
                q = Entity.query
                for attr in filters:
                    q = q.filter(getattr(Entity, attr).like("%%%s%%" % filters[attr]))
                objs = q.all()
            else:
                objs = Entity.query.all()

            return objs

        @api.doc(responses={
            200: 'Success'
        })
        def get(self):
            # pprint(json.loads(request.args['filters']))
            objs = self._query(request.args)
            result = get_collection_schema.dump(objs)
            return jsonify(result.data)

        @api.doc(
            body=resource_fields,
            responses={
                201: 'Created',
                422: 'Unprocessable entity'
            }
        )
        def post(self):
            self.pre_create()
            json_data = request.get_json(force=True)
            data, errors = post_schema.load(json_data)

            if any(errors):
                return make_response(jsonify(errors), 422)

            obj = Entity(data)
            db.session.add(obj)
            db.session.commit()
            self.post_create(obj)
            return make_response(jsonify(post_schema.dump(obj).data), 201)

        def pre_create(self):
            pass

        def post_create(self, obj):
            pass

    return CrudList
