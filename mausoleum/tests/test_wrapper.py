import pytest

from mausoleum import wrapper


@pytest.fixture
def name():
    return 'test.tomb'


@pytest.fixture
def size():
    return 10


@pytest.fixture
def key():
    return 'test.tomb.key'


def test_dig_tomb(name, size):
    