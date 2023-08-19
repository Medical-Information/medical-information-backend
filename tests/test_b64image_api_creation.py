import io
import os

import pytest
from django.contrib.auth import get_user_model
from django.core.files.images import ImageFile
from django.urls import reverse
from rest_framework import status

from articles.models import Article

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'image_file_name',
    [
        ('image_snapshot_jpg_4233_bytes.txt',),
        ('image_snapshot_jpg_5203_bytes.txt',),
    ],
)
def test_article_post_created(
    authenticated_client,
    article_content,
    settings,
    image_file_name,
):
    expected_article_count = Article.objects.count() + 1
    url = reverse('api:articles-list')
    with open(
        settings.BASE_DIR / 'tests' / 'fixtures' / 'snapshots' / image_file_name,
    ) as source:
        b64image = source.read()
    article_data = {}
    article_data.update(article_content)
    article_data['image'] = 'data:image;base64,' + b64image

    response = authenticated_client.post(url, article_data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Article.objects.count() == expected_article_count


@pytest.mark.parametrize(
    'image_file_name',
    [
        ('image_snapshot_gif.txt',),
        ('image_snapshot_approx_1700_kbytes.txt',),
    ],
)
def test_article_post_bad_request(
    authenticated_client,
    article_content,
    settings,
    image_file_name,
):
    expected_article_count = Article.objects.count()
    url = reverse('api:articles-list')
    with open(
        settings.BASE_DIR / 'tests' / 'fixtures' / 'snapshots' / image_file_name,
    ) as source:
        b64image = source.read()
    article_data = {}
    article_data.update(article_content)
    article_data['image'] = 'data:image;base64,' + b64image

    response = authenticated_client.post(url, article_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Article.objects.count() == expected_article_count


@pytest.mark.parametrize(
    'image_file_name',
    [
        ('image_snapshot_jpeg_100_100.txt',),
        ('image_snapshot_jpg_225_225.txt',),
    ],
)
def test_users_me_change_avatar_ok(
    alt_authenticated_client,
    alt_user,
    faker,
    settings,
    image_file_name,
):
    prefix = os.urandom(4).hex()
    old_avatar_name = f'avatar_name_{prefix}'
    old_avatar = ImageFile(file=io.BytesIO(faker.image()), name=old_avatar_name)
    alt_user.avatar = old_avatar
    alt_user.save()
    with open(
        settings.BASE_DIR / 'tests' / 'fixtures' / 'snapshots' / image_file_name,
    ) as source:
        b64image = source.read()
    url = reverse('api:users-me')
    new_data = {
        'avatar': b64image,
    }

    response = alt_authenticated_client.patch(url, new_data, format='json')

    alt_user.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data['avatar'] == 'http://testserver' + alt_user.avatar.url
    assert os.path.exists(settings.MEDIA_ROOT / alt_user.avatar.path)
    assert alt_user.avatar.name != old_avatar_name


@pytest.mark.parametrize(
    'image_file_name',
    [
        ('image_snapshot_gif.txt',),
        ('image_snapshot_png_3000_2596.txt',),
        ('image_snapshot_approx_1700_kbytes.txt',),
        ('image_snapshot_331_501.txt',),
    ],
)
def test_users_me_change_avatar_bad_request(
    alt_authenticated_client,
    alt_user,
    faker,
    settings,
    image_file_name,
):
    prefix = os.urandom(4).hex()
    old_avatar_name = f'avatar_name_{prefix}'
    old_avatar = ImageFile(file=io.BytesIO(faker.image()), name=old_avatar_name)
    alt_user.avatar = old_avatar
    alt_user.save()
    with open(
        settings.BASE_DIR / 'tests' / 'fixtures' / 'snapshots' / image_file_name,
    ) as source:
        b64image = source.read()
    url = reverse('api:users-me')
    new_data = {
        'avatar': b64image,
    }

    response = alt_authenticated_client.patch(url, new_data, format='json')

    alt_user.refresh_from_db()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert os.path.basename(alt_user.avatar.name) == old_avatar_name
