import subprocess

import click


def dig_tomb(name, size):
    """Dig a new tomb container."""
    return subprocess.run(['tomb', 'dig', '-s', str(size), name])


def forge_tomb(key, password):
    """Forge a new key for a tomb container."""
    return subprocess.run(['tomb', 'forge', '--unsafe', '--tomb-pwd', password, key])


def lock_tomb(name, key, password):
    """Lock a tomb container with the given key."""
    return subprocess.run(['tomb', 'lock', '--unsafe', '--tomb-pwd', password, name, '-k', key])


def open_tomb(name, key, password):
    """Open a tomb container with the given key."""
    return subprocess.run(['tomb', 'open', '--unsafe', '--tomb-pwd', password, name, '-k', key])


@click.group()
def cli():
    """Help"""


@cli.command()
@click.argument('name')
@click.argument('size')
@click.argument('key', required=False, default=None)
@click.password_option()
@click.option('--open', is_flag=True, help='Open a tomb after constructing it.')
def construct(name, size, key, password, open):
    construct = dig_tomb(name, size)
    if key is None:
        key = '{}.key' .format(name)
    fabricate = forge_tomb(key, password)
    if construct.returncode == 0 and fabricate.returncode == 0:
        lock_tomb(name, key, password)
        if open:
            open_tomb(name, key, password)


@cli.command()
@click.argument('name')
@click.argument('key', required=False, default=None)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False)
def enter(name, key, password):
    if key is None:
        key = '{}.key' .format(name)
    open_tomb(name, key, password)
