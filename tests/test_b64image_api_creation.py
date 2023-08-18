import io
import os

import pytest
from django.contrib.auth import get_user_model
from django.core.files.images import ImageFile
from django.urls import reverse

from articles.models import Article

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    ('image_file_name', 'expected_response_status_code'),
    [
        ('image_snapshot_gif.txt', 400),
        ('image_snapshot_jpg_4233_bytes.txt', 201),
        ('image_snapshot_jpg_5203_bytes.txt', 201),
        ('image_snapshot_approx_1700_kbytes.txt', 400),
    ],
)
def test_article_post(
    authenticated_client,
    article_content,
    settings,
    image_file_name,
    expected_response_status_code,
):
    initial_articles_count = Article.objects.count()
    if expected_response_status_code == 400:
        expected_article_count = initial_articles_count
    else:
        expected_article_count = initial_articles_count + 1

    url = reverse('api:articles-list')

    with open(
        settings.BASE_DIR / 'tests' / 'fixtures' / 'snapshots' / image_file_name,
    ) as source:
        b64image = source.read()

    article_data = {}
    article_data.update(article_content)
    article_data['image'] = 'data:image;base64,' + b64image

    response = authenticated_client.post(url, article_data, format='json')

    assert response.status_code == expected_response_status_code
    assert Article.objects.count() == expected_article_count


@pytest.mark.parametrize(
    ('image_file_name', 'expected_response_status_code'),
    [
        ('image_snapshot_gif.txt', 400),
        ('image_snapshot_jpeg_100_100.txt', 200),
        ('image_snapshot_jpg_225_225.txt', 200),
        ('image_snapshot_png_3000_2596.txt', 400),
        ('image_snapshot_approx_1700_kbytes.txt', 400),
        ('image_snapshot_331_501.txt', 400),
    ],
)
def test_users_me_change_avatar(
    alt_authenticated_client,
    alt_user,
    faker,
    settings,
    image_file_name,
    expected_response_status_code,
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
    assert response.status_code == expected_response_status_code

    if expected_response_status_code == 200:
        assert response.data['avatar'] == 'http://testserver' + alt_user.avatar.url
        assert os.path.exists(settings.MEDIA_ROOT / alt_user.avatar.path)
        assert alt_user.avatar.name != old_avatar_name

    if expected_response_status_code == 400:
        assert os.path.basename(alt_user.avatar.name) == old_avatar_name
