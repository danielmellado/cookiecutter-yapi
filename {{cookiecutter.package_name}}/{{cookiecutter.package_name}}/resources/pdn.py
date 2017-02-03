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

from .. import db, ma
from ..model import PDN as Entity
from .validation_util import validate_unique, validate_unique_update, \
    validate_ip, validate_exists

from .crud_resource import get_crud_resource, get_crud_list


class PdnSchema(ma.Schema):
    codigo = fields.String(required=True)
    descripcion = fields.String()
    ip_master = fields.String(validate=validate_ip)
    id_ubicacion = fields.Integer()

    @validates('codigo')
    def validate_codigo(self, value):
        validate_unique(db, Entity, 'codigo', value)

    @validates('id_ubicacion')
    def validate_ubicacion(self, value):
        validate_exists(db, Ubicacion, 'id', value)


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

PdnResource = get_crud_resource(db, Entity, get_schema, put_schema)
PdnList = get_crud_list(db, Entity, get_collection_schema, post_schema)
