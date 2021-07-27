#!/usr/bin/env python
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.append(PROJECT_ROOT)

import click
from src.common.click import add_click_commands
from src.data.scraping.main import scrape_cli


@add_click_commands(scrape_cli)
@click.group('jsim')
def cli():
    pass


def main(env_variables=None):
    """
    Run jewelsim command-line utilities within a custom environment.
    :param env_variables: dict
        The dictionary of custom environment variables: name -> value.
        These variables will be set before the command line execution
        and cleared right after it.
    """
    if env_variables is None:
        env_variables = {}

    _environ = os.environ.copy()
    try:
        os.environ.update(env_variables)
        cli()
    finally:
        os.environ.clear()
        os.environ.update(_environ)


if __name__ == '__main__':
    main(env_variables={
        'PROJECT_ROOT': PROJECT_ROOT,
        'PYTHONPATH': os.pathsep.join(sys.path),
    })
