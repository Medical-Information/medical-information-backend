import pytest
from django.db.models import Sum
from django.urls import reverse

from articles.models import Article, FavoriteArticle
from likes.models import Vote


@pytest.mark.django_db()
def test_article(authenticated_client, user, article_data):
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
    assert Article.objects.filter(pk=article_id).exists() is True

    url_add_like_unpublished = reverse(
        'api:articles-add-vote',
        args=(article_id, 'like'),
    )
    add_like_response_unpublished = authenticated_client.post(
        url_add_like_unpublished,
        {},
    )
    assert add_like_response_unpublished.status_code == 404

    article = Article.objects.get(pk=article_id)
    article.is_published = True
    article.save()

    url_add_like_published = reverse('api:articles-add-vote', args=(article_id, 'like'))
    add_like_response_published = authenticated_client.post(url_add_like_published, {})
    assert add_like_response_published.status_code == 200
    assert Vote.objects.count() == 1

    article.refresh_from_db()
    assert article.votes.count() == 1
    assert article.votes.aggregate(Sum('vote')).get('vote__sum') == 1
    assert user.likes.count() == 1
    assert user.likes.aggregate(Sum('vote')).get('vote__sum') == 1

    url_add_dislike_published = reverse(
        'api:articles-add-vote',
        args=(article_id, 'dislike'),
    )
    add_dislike_response_published = authenticated_client.post(
        url_add_dislike_published,
        {},
    )
    assert add_dislike_response_published.status_code == 200
    assert Vote.objects.count() == 1

    article.refresh_from_db()
    assert article.votes.count() == 1
    assert article.votes.aggregate(Sum('vote')).get('vote__sum') == -1
    assert user.likes.count() == 1
    assert user.likes.aggregate(Sum('vote')).get('vote__sum') == -1

    url_unvote = reverse('api:articles-unvote', args=(article_id,))
    unvote_response = authenticated_client.post(url_unvote, {})
    assert unvote_response.status_code == 200
    assert Vote.objects.count() == 0

    article.refresh_from_db()
    assert article.votes.count() == 0
    assert user.likes.count() == 0
