import click
from .{{cookiecutter.package_name}} import app


@app.cli.command()
def example_command():
    """
    This is an example command

    see http://flask.pocoo.org/docs/0.12/cli
    """
    click.echo('This is an example command')

