import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from model_bakery import baker

User = get_user_model()


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
