from click.testing import CliRunner
import pytest

from mausoleum import wrapper


@pytest.fixture(scope='session')
def password():
    """Use SUPER_SECURE_PASSWORD as the tomb password to pass to test functions."""
    return 'SUPER_SECURE_PASSWORD'


@pytest.fixture(scope='session')
def name():
    """Use test.tomb as the tomb name to pass to test functions."""
    return 'test.tomb'


@pytest.fixture(scope='session')
def key():
    """Use test.tomb.key as the tomb key name to pass to test functions."""
    return 'test.tomb.key'


@pytest.fixture(scope='session')
def tomb(name, key, password):
    """Setup the test.tomb so that other functions can use it."""
    wrapper.dig_tomb(name, 10)
    wrapper.forge_tomb(key, password, debug=True, kdf=1)
    wrapper.lock_tomb(name, key, password, debug=True)

    return name


@pytest.fixture(scope='session')
def second_tomb(password):
    """Another tomb to use in case multiple tombs are needed for a test."""
    tomb_path = 'test2.tomb'
    key_path = 'test2.tomb.key'

    wrapper.construct_tomb(tomb_path, 20, key_path, password, debug=True)

    return (tomb_path, key_path)


def test_cli_enter(tomb, password):
    """Test the enter CLI command."""
    runner = CliRunner()
    result = runner.invoke(wrapper.cli, ['enter', tomb, '--debug'], input=password)
    assert not result.exception

    assert '[test]' in wrapper.list_tombs()[0]

    wrapper.close_tomb(name='test')

    assert wrapper.list_tombs() == []

def test_read_only(name, key, password):
    """Test opening a tomb in read-only mode."""
    wrapper.open_tomb(name, key, password, debug=True, read_only=True, mountpoint='/media/test/mountpoint')
    assert '[test]' in wrapper.list_tombs()[0]

    wrapper.close_tomb(name='test')


def test_close_all_tombs(tomb, second_tomb, key, password):
    """Test closing multiple tombs."""
    wrapper.open_tomb(tomb, key, password, debug=True)
    wrapper.open_tomb(second_tomb[0], second_tomb[1], password, debug=True)

    assert len(wrapper.list_tombs()) == 2

    wrapper.close_tombs()

    assert wrapper.list_tombs() == []


def test_tomb_slam(tomb, key, password):
    """Test force closing a tomb."""
    wrapper.open_tomb(tomb, key, password, debug=True)
    assert '[test]' in wrapper.list_tombs()[0]

    wrapper.slam_tombs()

    assert wrapper.list_tombs() == []


def test_resize_tomb(tomb, key, password):
    """Test resizing the created tomb to 200mb."""
    wrapper.resize_tomb(tomb, 200, key, password)


def test_resize_cli_and_open(tomb, password):
    """Test the resize CLI command."""
    runner = CliRunner()
    result = runner.invoke(wrapper.cli, ['alter', '--open', '--debug', tomb, '200'], input=password)
    assert not result.exception

    result = runner.invoke(wrapper.cli, ['list'])
    assert 'test' in result.output

    result = runner.invoke(wrapper.cli, ['leave', 'test'])
    assert not result.exception


def test_cli_construct_and_close(password):
    """Test the construct CLI command."""
    runner = CliRunner()
    result = runner.invoke(wrapper.cli, ['construct', 'test3.tomb', '10', '--open', '--debug'], input=password)
    assert not result.exception

    result = runner.invoke(wrapper.cli, ['list'])
    assert 'test3' in result.output

    result = runner.invoke(wrapper.cli, ['leave', 'test3'])
    assert not result.exception


def test_cli_escape(tomb, password):
    """Test the escape CLI command."""
    runner = CliRunner()
    result = runner.invoke(wrapper.cli, ['enter', tomb, '--debug'], input=password)

    assert not result.exception

    result = runner.invoke(wrapper.cli, ['escape'])

    assert not result.exception


def test_cli_mold(key):
    """Test the mold CLI command which uses the engrave function."""
    runner = CliRunner()
    result = runner.invoke(wrapper.cli, ['mold', key])
    assert not result.exception


def test_cli_etch_and_resurrect(image_file, key, password):
    """Test the etch CLI command which uses the bury function.

    This tests two things: the embedding of a key inside an image and the extraction
    of a key from that image.
    """
    runner = CliRunner()

    result = runner.invoke(wrapper.cli, ['etch', image_file, key], input=password)
    assert not result.exception

    result = runner.invoke(wrapper.cli, ['resurrect', image_file], input=password)
    assert not result.exception
