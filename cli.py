#!/usr/bin/python3

import click
from core import commands


@click.group(context_settings={'help_option_names': ['-h', '--help']},
             help="Your CLI",
             commands=commands.get_pkg_commands('commands'))
def cli():
    pass


if __name__ == '__main__':
    cli()
