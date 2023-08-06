import base64

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from articles.models import Article


@pytest.fixture(autouse=True)
def _override_settings(settings, temp_dir):
    settings.MEDIA_ROOT = temp_dir


@pytest.mark.django_db()
def test_article_creation(faker, user):
    image = faker.image(image_format='jpeg')
    image_b64 = base64.b64encode(image)
    image_b64 = b'data:image;base64,' + image_b64
    article_data = {
        'title': faker.sentence(),
        'annotation': faker.sentence(),
        'text': faker.paragraph(5),
        'source_name': faker.sentence(3),
        'source_link': faker.url(),
        'image': image_b64,
    }

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse('api:articles-list')
    response = client.post(url, article_data, format='json')
    assert response.status_code == 201
    assert response.data['id'] is not None
    assert Article.objects.count() == 1
