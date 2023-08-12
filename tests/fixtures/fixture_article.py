import base64
import io
import os

import pytest
from django.core.files.images import ImageFile

from articles.models import Article


@pytest.fixture()
def b64_encoded_image(faker):
    image = faker.image(image_format='jpeg')
    image_b64 = base64.b64encode(image)
    return b'data:image;base64,' + image_b64


@pytest.fixture()
def article_content(faker):
    return {
        'title': faker.sentence(),
        'annotation': faker.sentence(),
        'text': faker.paragraph(5),
        'source_name': faker.sentence(3),
        'source_link': faker.url(),
    }


@pytest.fixture(autouse=True)
def article(faker, article_content, user):
    random_postfix = os.urandom(2).hex()
    image_file_bytes = io.BytesIO(faker.image(image_format='jpeg', size=(128, 128)))
    article = Article(**article_content)
    article.author = user
    article.image = ImageFile(
        file=image_file_bytes,
        name=f'test_file_{random_postfix}.jpeg',
    )
    article.save()
    yield article

    article.image.delete()
