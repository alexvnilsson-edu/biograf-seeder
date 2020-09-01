#!/usr/bin/env python

import click
import sys
import os
from os import path, getcwd
import shutil
from subprocess import run, PIPE
from argparse import ArgumentParser
from semver import SEMVER
from process import Process

python = "python3"


def git_check_tracked(path: str) -> bool:
    p = Process("git", "ls-files", "--error-unmatch", path, stdout=PIPE, stderr=PIPE)

    try:
        p.run()
        return True
    except Exception:
        return False


@click.group(name="package")
def package():
    pass


@package.command(name="clean")
@click.argument("paths", nargs=-1, type=click.Path(file_okay=True, dir_okay=True))
def clean(paths):
    cwd = getcwd()

    for d in paths:
        dp = path.join(cwd, d)

        if not git_check_tracked(dp):
            if path.exists(dp):
                if path.isdir(dp):
                    shutil.rmtree(path.join(cwd, d))
                elif path.isfile(dp):
                    os.remove(path.join(cwd, dp))
        else:
            print(
                f"Objektet {d} verkar tillhöra Git-indexet. Skippar osäker borttagning."
            )


@package.command(name="build")
@click.option("--verbose", is_flag=True, default=False)
def build(verbose: bool):
    p = Process(python, "setup.py", "sdist")

    if verbose:
        p.add_argument("--verbose")

    p.run()


@package.command(name="publish")
@click.option("--repository", type=click.STRING, default="testpypi")
@click.argument("dist", type=click.Path(resolve_path=False), required=True)
def publish(repository: str, dist: str):
    p = Process("twine", "upload")

    p.add_argument(f"--repository {repository}")
    p.add_argument(dist)

    print(p.cmd)

    p.run()


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
