#!/usr/bin/env python

import click
from subprocess import run
from argparse import ArgumentParser
from semver import SEMVER
from process import Process


@click.group(name="package")
def package():
    pass


@package.group(name="version")
def version():
    pass


@version.command(name="set")
@click.argument("new_version", required=True, type=SEMVER)
def set(new_version):
    print(new_version)


@version.command()
@click.argument(
    "increment", required=True, type=click.Choice(["major", "minor", "patch"])
)
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--verbose", is_flag=True, default=False)
def bump(increment: str, dry_run: bool, verbose: bool):
    p = Process("bumpversion", increment)

    if dry_run:
        p.add_argument("--dry-run", "--allow-dirty")

    if verbose:
        p.add_argument("--verbose")

    p.run()


if __name__ == "__main__":
    package()
