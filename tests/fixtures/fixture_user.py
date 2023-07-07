import pytest
from django.conf import settings
from django.test import Client
from model_bakery import baker

User = settings.AUTH_USER_MODEL


@pytest.fixture()
def client():
    return Client()


@pytest.fixture()
def user():
    return baker.make(User)


@pytest.fixture()
def authenticated_client(client, user):
    client.force_login(user)
    return client
