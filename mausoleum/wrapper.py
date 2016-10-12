import subprocess

import click


def dig_tomb(name, size):
    return subprocess.run(['tomb', 'dig', '-s', str(size), name])


def forge_tomb(key):
    return subprocess.run(['sudo', 'tomb', 'forge', key])


def lock_tomb(name, key):
    return subprocess.run(['tomb', 'lock', name, '-k', key])


@click.command()
@click.argument('name')
@click.argument('size')
@click.argument('key')
def cli(name, size, key):
    construct = dig_tomb(name, size)
    fabricate = forge_tomb(key)
    if construct.returncode == 0 and fabricate.returncode == 0:
        lock_tomb(name, key)

cli()
