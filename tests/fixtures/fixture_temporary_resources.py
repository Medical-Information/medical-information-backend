import os
import shutil

import pytest
from django.conf import settings as django_settings


@pytest.fixture(autouse=True, scope='session')
def temp_dir():
    random_suffix = os.urandom(4).hex()
    temp_dir = django_settings.BASE_DIR / f'test_temp_folder_{random_suffix}'
    os.mkdir(temp_dir)
    django_settings.MEDIA_ROOT = temp_dir
    yield temp_dir
    shutil.rmtree(temp_dir)
