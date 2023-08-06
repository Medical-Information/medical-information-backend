import os
import shutil

import pytest


@pytest.fixture()
def temp_dir(settings):
    random_suffix = os.urandom(4).hex()
    temp_dir = settings.BASE_DIR / f'test_temp_folder_{random_suffix}'
    os.mkdir(temp_dir)
    yield temp_dir
    shutil.rmtree(temp_dir)
