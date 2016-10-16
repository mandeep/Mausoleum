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
    wrapper.forge_tomb(key, password)


def test_lock_tomb(name, key, password):
    wrapper.lock_tomb(name, key, password)
