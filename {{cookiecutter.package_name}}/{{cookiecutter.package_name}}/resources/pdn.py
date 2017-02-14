"""
This module declares two flask_resources which have to be added
as entry points of the API in the file ``end_points.py``.

These resources are builded from the "templated" class defined in
crud_resource module.

The body parameters of the request for the operations post and put
are JSON string which are validated with marshmallow schemas (post_schema
and put_schema).

The get_schema and get_collection_schema are used by the operations
get resource and get collection in order to build a valid JSON as response

db is the database and Entity is the SQLAlchemy model to be managed by 
the CRUD.
"""

from marshmallow import fields, validates
from flask_restplus import fields as f

from .. import db, ma, api
from ..model import PDN as Entity
from .validation_util import validate_unique, validate_unique_update, \
    validate_ip, validate_exists

from .crud_resource import get_crud_resource, get_crud_list


"""
PdnSchema is a marshmallow schema

see: http://marshmallow.readthedocs.io/en/latest/
"""
class PdnSchema(ma.Schema):
    id = fields.Integer()
    codigo = fields.String(required=True)
    descripcion = fields.String()
    ip_master = fields.String(validate=validate_ip)
    id_ubicacion = fields.Integer()

    @validates('codigo')
    def validate_codigo(self, value):
        validate_unique(db, Entity, 'codigo', value)

"""
PdnUpdateSchema is an PdnSchema but with other features; codigo is not required
and the validation is a bit different
"""
class PdnUpdateSchema(PdnSchema):
    codigo = fields.String()

    @validates('codigo')
    def validate_codigo(self, value):
        validate_unique_update(db, Entity, 'codigo',
                               value, self.context['object'])


get_schema = PdnSchema()
get_collection_schema = PdnSchema(many=True)
post_schema = PdnSchema()
put_schema = PdnUpdateSchema()


"""
Unfortunately the swagger doc doesn't recognize the PdnSchema class to document the
body resource, so we have to define again the fields :-(.
I hope to see this feature in future release of flask-restplus

see: https://flask-restplus.readthedocs.io/en/stable/swagger.html
"""
resource_fields = api.model('Pdn', {
    'codigo': f.String(required=True),
    'descripcion': f.String,
    'ip_master': f.String,
    'id_ubicacion': f.Integer
 })

"""
These functions return Resource classes mapped against the database
"""
PdnBaseResource = get_crud_resource(db, Entity, get_schema, put_schema, resource_fields)
PdnBaseList = get_crud_list(db, Entity, get_collection_schema, post_schema, resource_fields)

"""
The resource class can't be shared between routes, that is, each route must have its own class.
So we define new child class.

see: https://flask-restplus.readthedocs.io/en/stable and module ``crud_resource.py`` in this
     package
"""
class PdnResource(PdnBaseResource):
    pass


class PdnList(PdnBaseList):
    pass
