import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

pytest_plugins = [
    'tests.fixtures.fixture_user',
    'tests.fixtures.fixture_temporary_resources',
]


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def authenticated_client(user):
    authenticated_client = APIClient()
    token, _ = Token.objects.get_or_create(user=user)
    authenticated_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return authenticated_client
