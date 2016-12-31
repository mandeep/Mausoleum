import subprocess

import click


def dig_tomb(name, size, path='tomb'):
    """Dig a new tomb container.

    Positional arguments:
    name -- the name of the container, e.g. secret.tomb
    size -- the size of the container in megabytes

    Keyword arguments:
    path -- the path to the tomb executable
    """
    return subprocess.call([path, 'dig', '-s', str(size), name])


def forge_tomb(key, password, path='tomb', kdf=0, sudo=None, debug=False):
    """Forge a new key for a tomb container.

    Positional arguments:
    key -- the name of the container's key, e.g. secret.tomb.key
    password -- the password to be used with the key

    Keyword arguments:
    path -- the path to the tomb executable
    kdf -- number of KDF iterations to perform, default is 0
    sudo -- the sudo password of the current admin, default is None
    debug -- used to test key generation
    """
    arguments = ['sudo', '--stdin', path, 'forge', '--unsafe', '--tomb-pwd', password, key]
    if debug:
        arguments.extend(['--ignore-swap', '--use-urandom'])
    if kdf > 0:
        arguments.extend(['--kdf', str(kdf)])
    if sudo is not None:
        forge_command = subprocess.Popen(arguments, stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE, universal_newlines=True)
        return forge_command.communicate(sudo + '\n')
    return subprocess.call(arguments)


def lock_tomb(name, key, password, path='tomb', sudo=None, debug=False):
    """Lock a tomb container with the given key.

    Positional arguments:
    name -- the name of the container, e.g. secret.tomb
    key -- the name of the container's key, e.g. secret.tomb.key
    password -- the password of the container's key

    Keyword arguments:
    path -- the path to the tomb executable
    sudo -- the sudo password of the current admin, default is None
    debug -- used to ignore the swap partition
    """
    arguments = ['sudo', '--stdin', path, 'lock', '--unsafe', '--tomb-pwd',
                 password, name, '-k', key]
    if debug:
        arguments.append('--ignore-swap')
    if sudo is not None:
        lock_command = subprocess.Popen(arguments, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, universal_newlines=True)
        return lock_command.communicate(sudo + '\n')
    return subprocess.call(arguments)


def construct_tomb(name, size, key, password, debug=False):
    """Dig, forge, and lock a tomb container with the given key.

    Positional arguments:
    name -- the name of the container, e.g. secret.tomb
    key -- the name of the container's key, e.g. secret.tomb.key
    password -- the password of the container's key
    """
    construction = dig_tomb(name, size)
    if key is None:
        key = '{}.key' .format(name)
    if construction == 0:
        if debug:
            fabrication = forge_tomb(key, password, debug=True)
        else:
            fabrication = forge_tomb(key, password)
        if fabrication == 0:
            lock_tomb(name, key, password)


def open_tomb(name, key, password, path='tomb', read_only=False, sudo=None):
    """Open a tomb container with the given key.

    Positional arguments:
    name -- the name of the container, e.g. secret.tomb
    key -- the name of the container's key, e.g. secret.tomb.key
    password -- the password of the container's key

    Keyword arguments:
    path -- the path to the tomb executable
    read_only -- mount the tomb as read only
    sudo -- the sudo password of the current admin, default is None
    """
    arguments = ['sudo', '--stdin', path, 'open', '--unsafe',
                 '--tomb-pwd', password, name, '-k', key]
    if read_only:
        arguments.extend(['-o', 'ro'])
    if sudo is not None:
        open_command = subprocess.Popen(arguments, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, universal_newlines=True)
        return open_command.communicate(sudo + '\n')
    return subprocess.call(arguments)


def resize_tomb(name, size, key, password, path='tomb'):
    """Resize a tomb container to the given size.

    Positional arguments:
    name -- the name of the container, e.g. secret.tomb
    size -- the size of the container in megabytes
    key -- the name of the container's key, e.g. secret.tomb.key
    password -- the password of the container's key

    Keyword arguments:
    path -- the path to the tomb executable
    """
    return subprocess.call([path, 'resize', name, '-s', str(size), '-k', key, '--unsafe',
                            '--tomb-pwd', password])


def list_tombs(path='tomb'):
    """Create a list of all open tombs.

    Keyword argument:
    path -- the path to the tomb executable
    """
    try:
        tomb_output = subprocess.check_output([path, 'list', '--no-color'],
                                              stderr=subprocess.STDOUT,
                                              universal_newlines=True).split('\n')
        return [line.replace('tomb  .  ', '') for line in tomb_output if 'open on' in line]
    except subprocess.CalledProcessError:
        return []


def close_tomb(path='tomb', name=''):
    """Close an open tomb container.

    Keyword arguments:
    path -- the path to the tomb executable
    name -- the name of the container to close (if multiple tombs are open)
    """
    return subprocess.call([path, 'close', name])


def close_tombs(path='tomb'):
    """Close all open tombs.

    Keyword argument:
    path -- the path to the tomb executable
    """
    return subprocess.call([path, 'close', 'all'])


def slam_tombs(path='tomb'):
    """Force close all open tombs.

    Keyword argument:
    path -- the path to the tomb executable
    """
    return subprocess.call([path, 'slam'])


@click.group()
def cli():
    """Access Tomb's command line interface with Mausoleum.

    Mausoleum includes multiple commands that wrap around Tomb's command line interface:
    $  mausoleum construct [OPTIONS] NAME SIZE [KEY]
    $  mausoleum enter [OPTIONS] NAME [KEY]
    $  mausoleum alter [OPTIONS] NAME SIZE [KEY]

    To create and open a new 500MB tomb container and key, run:
    $  mausoleum construct --open secret.tomb 500

    To open an existing tomb container, run:
    $  mausoleum enter secret.tomb

    To resize an existing tomb container to 20MB, run:
    $  mausoleum alter secret.tomb 20
    """


@cli.command()
@click.argument('name')
@click.argument('size')
@click.argument('key', required=False, default=None)
@click.password_option()
@click.option('--open', is_flag=True, help='Open a tomb after constructing it.')
def construct(name, size, key, password, open):
    """Dig, forge, and lock a new tomb container.

    The default key name is the name of the tomb with .key appended as the suffix. If
    you would like the key to use a different naming convention, it must be passed as an
    argument.

    To open the container after creation, use the --open flag.
    """
    construct_tomb(name, size, key, password)
    if open:
        open_tomb(name, key, password)


@cli.command()
@click.argument('name')
@click.argument('key', required=False, default=None)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False)
def enter(name, key, password):
    """Open an existing tomb container.

    The default key name is the name of the tomb with .key as the suffix. If the
    key uses a different naming convention, it must be passed as an argument.
    """
    if key is None:
        key = '{}.key' .format(name)
    open_tomb(name, key, password)


@cli.command()
@click.argument('name')
@click.argument('size')
@click.argument('key', required=False, default=None)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False)
@click.option('--open', is_flag=True, help='Open the tomb after resizing it.')
def alter(name, size, key, password, open):
    """Resize an existing tomb container.

    The default key name is the name of the tomb with .key as the suffix. If the
    key uses a different naming convention, it must be passed as an argument.

    To open the container after resizing, use the --open flag.
    """
    if key is None:
        key = '{}.key' .format(name)
    resize_tomb(name, str(size), key, password)
    if open:
        open_tomb(name, key, password)
