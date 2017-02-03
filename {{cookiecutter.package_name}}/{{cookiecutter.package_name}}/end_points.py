from .resources.foo import Foo
from .resources.pdn import PdnList, PdnResource
from .{{cookiecutter.package_name}} import api


def create_endpoints():
    """Creates the endpoints (routes) to the API resources"""
    api.add_resource(Foo, '/foo')
    api.add_resource(PdnList, '/pdn')
    api.add_resource(PdnResource, '/pdn/<int:id>')
