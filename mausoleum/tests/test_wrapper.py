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


def test_tomb_creation(name, key, password):
    """Test the creation of a tomb contanier.

    All three functions are tested here due to a bug in click's
    CliRunner that does not allow two inputs for the password prompt.
    """
    dig = wrapper.dig_tomb(name, 10)
    if dig == 0:
        forge = wrapper.forge_tomb(key, password)
        if forge == 0:
            wrapper.lock_tomb(name, key, password)
