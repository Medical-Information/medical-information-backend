import io
import os

import pytest
from django.contrib.auth import get_user_model
from django.core.files.images import ImageFile
from django.urls import reverse

User = get_user_model()

pytestmark = pytest.mark.django_db


def test_user_creation_by_api(faker, client, user_credentials_api):
    user_url = reverse('api:users-list')
    password = faker.password()
    user_credentials_api.update(
        {'password': password, 're_password': password},
    )
    response = client.post(user_url, user_credentials_api)

    assert response.status_code == 201
    assert response.data['id'] is not None
    assert response.data['first_name'] == user_credentials_api['first_name']
    assert response.data['last_name'] == user_credentials_api['last_name']
    assert response.data['email'] == user_credentials_api['email']


def test_user_creation_by_api_short_password(faker, client, user_credentials_api):
    user_url = reverse('api:users-list')
    password = faker.password(4)
    user_credentials_api.update(
        {'password': password, 're_password': password},
    )

    too_short_password_response = client.post(user_url, user_credentials_api)

    assert too_short_password_response.status_code == 400


def test_user_creation_by_api_long_password(faker, client, user_credentials_api):
    user_url = reverse('api:users-list')
    password = faker.password(24)
    user_credentials_api.update(
        {'password': password, 're_password': password},
    )

    too_long_password_response = client.post(user_url, user_credentials_api)

    assert too_long_password_response.status_code == 400


def test_user_creation_by_api_email_regression(client):
    url = reverse('api:users-list')
    user_data = {
        'first_name': 'ФфRr',
        'last_name': 'RRФф',
        'email': 'SS#%&@example.com',
        'password': '123456',
        're_password': '123456',
    }

    response = client.post(url, user_data, format='json')

    assert response.status_code == 400
    assert User.objects.filter(email=user_data['email']).exists() is False


def test_login(client, user_credentials):
    login_url = reverse('api:login')
    response = client.post(login_url, user_credentials)

    assert response.status_code == 200
    assert response.data['auth_token'] is not None


def test_users_list_admin(authenticated_client, user):
    """No pagination."""
    url = reverse('api:users-list')
    user.is_staff = True
    user.save()

    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == User.objects.count()


def test_users_list_user(alt_authenticated_client, alt_user):
    """No pagination."""
    url = reverse('api:users-list')

    response = alt_authenticated_client.get(url)

    assert response.status_code == 200
    assert response.data[0]['id'] == str(alt_user.pk)
    assert len(response.data) == 1


def test_users_list_anonymous(client):
    url = reverse('api:users-list')

    response = client.get(url)

    assert response.status_code == 401


def test_users_get(alt_authenticated_client, user):
    url = reverse('api:users-detail', args=(str(user.pk),))

    response = alt_authenticated_client.get(url)

    assert response.status_code == 404


def test_users_me_authenticated(alt_authenticated_client, alt_user):
    url = reverse('api:users-me')

    response = alt_authenticated_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == str(alt_user.pk)
    assert 'first_name' in response.data
    assert 'last_name' in response.data
    assert 'role' in response.data
    assert 'email' in response.data
    assert 'avatar' in response.data
    assert 'rating' in response.data
    assert 'publications_amount' in response.data
    assert 'subscribed' in response.data


def test_users_me_anonymous(client):
    url = reverse('api:users-me')

    response = client.get(url)

    assert response.status_code == 401


def test_users_me_patch(
    alt_authenticated_client,
    alt_user,
    faker,
    b64_encoded_image,
    settings,
):
    url = reverse('api:users-me')
    first_name = faker.first_name()
    last_name = faker.last_name()
    new_data = {
        'first_name': first_name,
        'last_name': last_name,
        'avatar': b64_encoded_image,
    }

    response = alt_authenticated_client.patch(url, new_data, format='json')
    alt_user.refresh_from_db()

    assert response.status_code == 200
    assert response.data['id'] == str(alt_user.pk)
    assert response.data['first_name'] == first_name
    assert response.data['last_name'] == last_name
    assert response.data['rating'] == 0
    assert response.data['publications_amount'] == 0
    assert response.data['subscribed'] is False
    assert response.data['avatar'] is not None
    assert alt_user.first_name == first_name
    assert alt_user.last_name == last_name
    assert alt_user.avatar is not None
    assert os.path.exists(settings.MEDIA_ROOT / alt_user.avatar.path)


def test_users_me_change_avatar(
    alt_authenticated_client,
    alt_user,
    faker,
    b64_encoded_image,
    settings,
):
    old_avatar_name = 'avatar_name'
    old_avatar = ImageFile(file=io.BytesIO(faker.image()), name=old_avatar_name)
    alt_user.avatar = old_avatar
    alt_user.save()
    url = reverse('api:users-me')
    new_data = {
        'avatar': b64_encoded_image,
    }

    response = alt_authenticated_client.patch(url, new_data, format='json')

    alt_user.refresh_from_db()
    assert response.status_code == 200
    assert response.data['avatar'] == 'http://testserver' + alt_user.avatar.url
    assert os.path.exists(settings.MEDIA_ROOT / alt_user.avatar.path)
    assert alt_user.avatar.name != old_avatar_name


def test_users_me_publications_amount(authenticated_client, user):
    url = reverse('api:users-me')

    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert response.data['publications_amount'] == user.articles.count()


def test_users_me_put(alt_authenticated_client, faker):
    url = reverse('api:users-me')
    first_name = faker.first_name()
    last_name = faker.last_name()
    new_data = {
        'first_name': first_name,
        'last_name': last_name,
    }

    response = alt_authenticated_client.put(url, new_data, format='json')

    assert response.status_code == 405


def test_users_me_delete(alt_authenticated_client, faker):
    url = reverse('api:users-me')

    response = alt_authenticated_client.put(url)

    assert response.status_code == 405


def test_user_set_password(faker, authenticated_client, user, user_credentials):
    url = reverse('api:users-set-password')
    new_password = faker.password(16)
    password_data = {
        'new_password': new_password,
        'current_password': user_credentials['password'],
    }

    response = authenticated_client.post(url, password_data, format='json')

    user.refresh_from_db()
    assert response.status_code == 204
    assert user.check_password(password_data['current_password']) is False
    assert user.check_password(password_data['new_password']) is True


def test_user_set_password_short_password(
    faker,
    authenticated_client,
    user,
    user_credentials,
):
    url = reverse('api:users-set-password')
    new_password = faker.password(4)
    password_data = {
        'new_password': new_password,
        'current_password': user_credentials['password'],
    }

    response = authenticated_client.post(url, password_data, format='json')

    user.refresh_from_db()
    assert response.status_code == 400
    assert user.check_password(password_data['current_password']) is True
    assert user.check_password(password_data['new_password']) is False


def test_user_set_password_long_password(
    faker,
    authenticated_client,
    user,
    user_credentials,
):
    url = reverse('api:users-set-password')
    new_password = faker.password(24)
    password_data = {
        'new_password': new_password,
        'current_password': user_credentials['password'],
    }

    response = authenticated_client.post(url, password_data, format='json')

    user.refresh_from_db()
    assert response.status_code == 400
    assert user.check_password(password_data['current_password']) is True
    assert user.check_password(password_data['new_password']) is False


def test_subscription_anonymous(client):
    url = reverse('api:users-subscription')

    response = client.patch(url)

    assert response.status_code == 401


def test_subscription_authenticated(authenticated_client, user):
    url = reverse('api:users-subscription')

    response = authenticated_client.patch(url)

    user.refresh_from_db()
    assert response.status_code == 204
    assert user.subscribed is True


def test_subscription_duplicated(authenticated_client, user):
    url = reverse('api:users-subscription')
    user.subscribed = True
    user.save()

    response = authenticated_client.patch(url)

    user.refresh_from_db()
    assert response.status_code == 400
    assert user.subscribed is True


def test_unsubscription(authenticated_client, user):
    url = reverse('api:users-subscription')
    user.subscribed = True
    user.save()

    response = authenticated_client.delete(url)

    user.refresh_from_db()
    assert response.status_code == 204
    assert user.subscribed is False


def test_unexisted_unsubscription(authenticated_client, user):
    url = reverse('api:users-subscription')

    response = authenticated_client.delete(url)

    user.refresh_from_db()
    assert response.status_code == 400
    assert user.subscribed is False


def test_password_change_space_character(authenticated_client, user):
    url = reverse('api:users-set-password')
    password_data = {
        'new_password': '123 456',
        'current_password': '123456%',
    }
    user.set_password(password_data['current_password'])
    user.save()

    response = authenticated_client.post(url, password_data, format='json')

    user.refresh_from_db()
    assert response.status_code == 400
    assert user.password is not None
    assert user.check_password(password_data['current_password']) is True
    assert user.check_password(password_data['new_password']) is False
