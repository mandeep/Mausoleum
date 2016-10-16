from click.testing import CliRunner
import pytest

from mausoleum import wrapper


@pytest.fixture
def name():
    return 'test.tomb'


@pytest.fixture
def key():
    return 'test.tomb.key'


@pytest.fixture
def password():
    return 'SUPER_SECURE_PASSWORD'


def test_dig_tomb(name):
    wrapper.dig_tomb(name, 10)


def test_forge_tomb(key, password):
    wrapper.forge_tomb(key, password, debug=True)


def test_lock_tomb(name, key, password):
    wrapper.lock_tomb(name, key, password, debug=True)


def test_cli_enter(name, password):
    runner = CliRunner()
    result = runner.invoke(wrapper.cli, ['enter', name], input=password)
    assert not result.exception


def test_close_tomb():
    wrapper.close_tomb()


def test_close_all_tombs(name, key, password):
    wrapper.open_tomb(name, key, password)
    wrapper.close_tombs()
