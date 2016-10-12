import subprocess

import click


def dig_tomb(name, size):
    return subprocess.run(['tomb', 'dig', '-s', str(size), name])


def forge_tomb(key):
    return subprocess.run(['sudo', 'tomb', 'forge', key])


def lock_tomb(name, key):
    return subprocess.run(['tomb', 'lock', name, '-k', key])


@click.group()
def cli():
    """Help"""


@cli.command()
@click.argument('name')
@click.argument('size')
@click.argument('key', required=False, default=None)
def construct(name, size, key):
    construct = dig_tomb(name, size)
    if key is None:
        key = '{}.key' .format(name)
    fabricate = forge_tomb(key)
    if construct.returncode == 0 and fabricate.returncode == 0:
        lock_tomb(name, key)
