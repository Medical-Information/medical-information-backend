import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture()
def user_credentials_api(faker):
    return {
        'first_name': faker.first_name(),
        'last_name': faker.last_name(),
        'email': faker.email(),
    }


@pytest.fixture()
def user_credentials():
    return {
        'email': 'test_email',
        'password': 'test_password',
    }


@pytest.fixture()
def alt_user_credentials():
    return {
        'email': 'alt_test_email',
        'password': 'alt_test_password',
    }


@pytest.fixture(autouse=True)
def user(db, user_credentials):
    user = User.objects.create_user(**user_credentials)
    user.is_active = True
    user.is_staff = True
    user.save()
    return user


@pytest.fixture(autouse=True)
def alt_user(db, alt_user_credentials):
    alt_user = User.objects.create_user(**alt_user_credentials)
    alt_user.is_active = True
    alt_user.save()
    return alt_user
