import os
import shutil

import pytest


@pytest.fixture(autouse=True, scope="session")
def tmp_dir(tmpdir_factory):
    directory = tmpdir_factory.mktemp('test')
    os.chdir(str(directory))
    yield directory
    shutil.rmtree(str(directory), ignore_errors=True)


@pytest.fixture
def image_file(tmp_dir):
    """Pass a JPEG file resource as an argument to the unit tests."""
    file = os.path.join(os.path.dirname(__file__), 'test.jpg')
    test_file = str(tmp_dir.join('test.jpg'))
    shutil.copyfile(file, test_file)

    return test_file
