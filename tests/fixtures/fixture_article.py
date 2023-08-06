import base64

import pytest


@pytest.fixture()
def article_data(faker):
    image = faker.image(image_format='jpeg')
    image_b64 = base64.b64encode(image)
    image_b64 = b'data:image;base64,' + image_b64
    return {
        'title': faker.sentence(),
        'annotation': faker.sentence(),
        'text': faker.paragraph(5),
        'source_name': faker.sentence(3),
        'source_link': faker.url(),
        'image': image_b64,
    }
