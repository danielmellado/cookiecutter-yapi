import click
from .{{cookiecutter.package_name}} import app, api


@app.cli.command()
def example_command():
    """
    This is an example command

    see http://flask.pocoo.org/docs/0.12/cli
    """
    click.echo('This is an example command')

app.config['SERVER_NAME'] = 'localhost:5000'

@app.cli.command()
def export_api():
    """To help you testing, you can export your API as a Postman collection."""
    with app.app_context():
        urlvars = False  # Build query strings in URLs
        swagger = True  # Export Swagger specifications
        data = api.as_postman(urlvars=urlvars, swagger=swagger)
        f = open('postman_import.json', 'w')
        f.write(json.dumps(data))