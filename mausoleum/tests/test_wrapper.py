import pkg_resources

from click.testing import CliRunner
import pytest

from mausoleum import wrapper


@pytest.fixture
def name():
    """Use test.tomb as the tomb name to pass to test functions."""
    return 'test.tomb'


@pytest.fixture
def key():
    """Use test.tomb.key as the tomb key name to pass to test functions."""
    return 'test.tomb.key'


@pytest.fixture
def password():
    """Use SUPER_SECURE_PASSWORD as the tomb password to pass to test functions."""
    return 'SUPER_SECURE_PASSWORD'


@pytest.fixture
def image_file():
    """Pass a JPEG file resource as an argument to the unit tests."""
    file = pkg_resources.resource_filename('mausoleum.tests', 'test.jpg')
    return file


def test_dig_tomb(name):
    """Test creation of a new tomb container with a size of 10mb."""
    wrapper.dig_tomb(name, 10)


def test_forge_tomb(key, password):
    """Test creation of a new tomb key for the created tomb container."""
    wrapper.forge_tomb(key, password, debug=True)


@pytest.mark.xfail()
def test_lock_tomb(name, key, password):
    """Test locking the tomb container with the created key.

    This test is marked as xfail as this Travis throws an erroneous
    error during testing.
    """
    wrapper.lock_tomb(name, key, password, debug=True)


def test_construct_tomb(name, key, password,):
    """Test constructing a new tomb container."""
    wrapper.construct_tomb('test2.tomb', 20, 'test2.tomb.key', password, debug=True)


def test_cli_enter(name, password):
    """Test the enter CLI command."""
    runner = CliRunner()
    result = runner.invoke(wrapper.cli, ['enter', name], input=password)
    assert not result.exception


def test_list_tombs():
    """Test that opened tombs are discovered."""
    assert '[test]' in wrapper.list_tombs()[0]


def test_close_tomb():
    """Test closing the created tomb."""
    wrapper.close_tomb()
    assert wrapper.list_tombs() == []


def test_close_all_tombs(name, key, password):
    """Test closing a tomb by opening the created tomb container."""
    wrapper.open_tomb(name, key, password)
    wrapper.close_tombs()


def test_tomb_slam(name, key, password):
    """Test force closing a tomb by opening the create tomb container."""
    wrapper.open_tomb(name, key, password)
    wrapper.slam_tombs()


def test_resize_tomb(name, key, password):
    """Test resizing the created tomb to 20mb."""
    wrapper.resize_tomb(name, 20, key, password)


def test_resize_cli(name, password):
    """Test the resize CLI command."""
    runner = CliRunner()
    result = runner.invoke(wrapper.cli, ['alter', '--open', name, '30'], input=password)
    assert not result.exception


def test_cli_mold(key):
    """Test the mold CLI command which uses the engrave function."""
    runner = CliRunner()
    result = runner.invoke(wrapper.cli, ['mold', key])
    assert not result.exception


def test_cli_etch(image_file, key, password):
    """Test the etch CLI command which uses the bury function."""
    runner = CliRunner()
    result = runner.invoke(wrapper.cli, ['etch', image_file, key], input=password)
    assert not result.exception


def test_cli_resurrect(image_file, password):
    """Test the resurrect CLI command which uses the exhume function."""
    runner = CliRunner()
    result = runner.invoke(wrapper.cli, ['resurrect', image_file], input=password)
    assert not result.exception
