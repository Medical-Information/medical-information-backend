import base64

import pytest
from django.urls import reverse

from articles.models import Article, FavoriteArticle


@pytest.mark.django_db()
def test_article(faker, authenticated_client, user):
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
    url = reverse('api:articles-list')
    response = authenticated_client.post(url, article_data, format='json')

    assert response.status_code == 201
    assert response.data['id'] is not None
    assert Article.objects.count() == 1

    article_id = response.data['id']
    favorite_url = reverse('api:articles-favorite', args=(article_id,))
    fav_response = authenticated_client.post(favorite_url)

    assert fav_response.status_code == 201
    assert user.favorite_articles.filter(article__pk=article_id).exists() is True
    assert user.favorite_articles.count() == 1

    fav_response_duplicated = authenticated_client.post(favorite_url)

    assert fav_response_duplicated.status_code == 400
    assert user.favorite_articles.count() == 1
    assert (
        FavoriteArticle.objects.filter(
            user=user,
            article__pk=article_id,
        ).count()
        == 1
    )

    fav_response_delete = authenticated_client.delete(favorite_url)

    assert fav_response_delete.status_code == 204
    assert user.favorite_articles.filter(article__pk=article_id).exists() is False
    assert user.favorite_articles.count() == 0

    fav_response_delete_duplicated = authenticated_client.delete(favorite_url)

    assert fav_response_delete_duplicated.status_code == 400
    assert user.favorite_articles.filter(article__pk=article_id).exists() is False
    assert user.favorite_articles.count() == 0
    assert (
        FavoriteArticle.objects.filter(
            user=user,
            article__pk=article_id,
        ).count()
        == 0
    )
