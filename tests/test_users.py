import pytest
from django.urls import reverse


@pytest.mark.django_db()
def test_user_creation_by_api(faker, client):
    user_url = reverse('api:users-list')
    password = faker.password()
    user_credentials = {
        'first_name': faker.first_name(),
        'last_name': faker.last_name(),
        'email': faker.email(),
        'password': password,
        're_password': password,
    }
    successful_response = client.post(user_url, user_credentials)

    assert successful_response.status_code == 201
    assert successful_response.data['id'] is not None

    too_short_password = faker.password(4)
    user_credentials['password'] = too_short_password
    too_short_password_response = client.post(user_url, user_credentials)

    assert too_short_password_response.status_code == 400

    too_long_password = faker.password(24)
    user_credentials['password'] = too_long_password
    too_long_password_response = client.post(user_url, user_credentials)

    assert too_long_password_response.status_code == 400


@pytest.mark.django_db()
def test_login(client, user_credentials):
    login_url = reverse('api:login')
    response = client.post(login_url, user_credentials)

    assert response.status_code == 200
    assert response.data['auth_token'] is not None
