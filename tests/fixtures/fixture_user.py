import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture()
def user_credentials():
    return {
        'email': 'test_email',
        'password': 'test_password',
    }


@pytest.fixture(autouse=True)
def user(db, user_credentials):
    user = User.objects.create_user(**user_credentials)
    user.is_active = True
    user.save()
    return user
