from unittest.mock import Mock

import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import Client as DjangoTestClient
from django.urls import reverse

from users.admin import UserAdmin
from users.models import RolesTypes

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.fixture()
def user_creation_form():
    admin_site = AdminSite()
    user_admin = UserAdmin(User, admin_site)
    request = Mock()
    form = user_admin.get_form(request)
    return form


@pytest.fixture()
def user_data():
    return {
        'email': 'example@example.com',
        'password1': 'example@example.com',
        'password2': 'example@example.com',
        'first_name': 'exampleexamplecom',
        'last_name': 'exampleexamplecom',
        'role': RolesTypes.USER,
    }


def test_admin_site_user_creation_success(user_creation_form, user_data):
    form = user_creation_form(user_data)

    assert form.is_valid()
    assert form._errors == {}


def test_admin_site_user_creation_failure(user_creation_form, user_data):
    user_data.pop('last_name')
    form = user_creation_form(user_data)

    assert form.is_valid() is False
    assert form._errors == {'last_name': ['Обязательное поле.']}


def test_admin_form_creation_success(user, user_data):
    initial_count = User.objects.count()

    user.is_superuser = True
    user.is_staff = True
    user.save()

    url = reverse('admin:users_user_add')

    client = DjangoTestClient()
    client.force_login(user=user)

    response = client.post(url, data=user_data, follow=True)

    assert response.status_code == 200
    assert User.objects.count() == initial_count + 1
    assert User.objects.filter(email=user_data['email']).exists() is True


def test_admin_form_creation_failure(user, user_data):
    initial_count = User.objects.count()
    user_data.pop('last_name')

    user.is_superuser = True
    user.is_staff = True
    user.save()

    url = reverse('admin:users_user_add')

    client = DjangoTestClient()
    client.force_login(user=user)

    response = client.post(url, data=user_data, follow=True)

    assert len(response.context_data['errors']) != 0
    assert response.context_data['errors'][0].data[0].message == 'Обязательное поле.'
    assert User.objects.count() == initial_count
    assert User.objects.filter(email=user_data['email']).exists() is False
