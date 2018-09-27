import os

import pytest


@pytest.fixture(autouse=True, scope="session")
def tmp_dir(tmpdir_factory):
    directory = tmpdir_factory.mktemp('test')
    os.chdir(str(directory))
