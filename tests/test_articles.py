import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from articles.models import Article, FavoriteArticle
from likes.models import VoteTypes
from likes.services import add_vote

User = get_user_model()

pytestmark = pytest.mark.django_db


def test_article_post(authenticated_client, article_content, article_image):
    """Article creation though API with POST method."""
    url = reverse('api:articles-list')
    article_data = {}
    article_data.update(article_content)
    article_data['image'] = article_image

    response = authenticated_client.post(url, article_data, format='json')

    assert response.status_code == 201
    assert response.data['id'] is not None
    assert Article.objects.filter(pk=response.data['id']).exists() is True


def test_wrong_vote_type_own_article(authenticated_client, article):
    article.is_published = True
    article.save()
    vote_value = 'wrong_type'
    url = reverse('api:articles-add-vote', args=(article.pk, vote_value))

    response = authenticated_client.post(url)

    assert response.status_code == 403


def test_wrong_vote_type_not_own_article(alt_authenticated_client, article):
    article.is_published = True
    article.save()
    vote_value = 'wrong_type'
    url = reverse('api:articles-add-vote', args=(article.pk, vote_value))

    response = alt_authenticated_client.post(url)

    assert response.status_code == 400


def test_like_own_unpublished_article(authenticated_client, user, article):
    url = reverse('api:articles-add-vote', args=(article.pk, 'like'))

    response = authenticated_client.post(url)

    assert response.status_code == 404
    assert article.votes.filter(user=user, vote=VoteTypes.LIKE).exists() is False


def test_dislike_own_unpublished_article(authenticated_client, user, article):
    url = reverse('api:articles-add-vote', args=(article.pk, 'dislike'))

    response = authenticated_client.post(url)

    assert response.status_code == 404
    assert article.votes.filter(user=user, vote=VoteTypes.DISLIKE).exists() is False


def test_like_own_published_article(authenticated_client, user, article):
    article.is_published = True
    article.save()
    url = reverse('api:articles-add-vote', args=(article.pk, 'like'))

    response = authenticated_client.post(url)

    assert response.status_code == 403
    assert article.votes.filter(user=user, vote=VoteTypes.LIKE).exists() is False


def test_dislike_own_published_article(authenticated_client, user, article):
    article.is_published = True
    article.save()
    url = reverse('api:articles-add-vote', args=(article.pk, 'dislike'))

    response = authenticated_client.post(url)

    assert response.status_code == 403
    assert article.votes.filter(user=user, vote=VoteTypes.DISLIKE).exists() is False


def test_unvote_own_unpublished_article(authenticated_client, article):
    url = reverse('api:articles-unvote', args=(article.pk,))

    response = authenticated_client.post(url)

    assert response.status_code == 404


def test_unvote_own_published_article(authenticated_client, article):
    article.is_published = True
    article.save()
    url = reverse('api:articles-unvote', args=(article.pk,))

    response = authenticated_client.post(url)

    assert response.status_code == 403


def test_like_unpublished_article(alt_authenticated_client, alt_user, article):
    url = reverse('api:articles-add-vote', args=(article.pk, 'like'))

    response = alt_authenticated_client.post(url)

    assert response.status_code == 404
    assert article.votes.filter(user=alt_user, vote=VoteTypes.LIKE).exists() is False


def test_like_published_article(alt_authenticated_client, alt_user, article):
    article.is_published = True
    article.save()
    url = reverse('api:articles-add-vote', args=(article.pk, 'like'))

    response = alt_authenticated_client.post(url)

    assert response.status_code == 204
    assert article.votes.filter(user=alt_user, vote=VoteTypes.LIKE).exists() is True


def test_dislike_unpublished_article(alt_authenticated_client, alt_user, article):
    url = reverse('api:articles-add-vote', args=(article.pk, 'dislike'))

    response = alt_authenticated_client.post(url)

    assert response.status_code == 404
    assert article.votes.filter(user=alt_user, vote=VoteTypes.DISLIKE).exists() is False


def test_dislike_published_article(alt_authenticated_client, alt_user, article):
    article.is_published = True
    article.save()
    url = reverse('api:articles-add-vote', args=(article.pk, 'dislike'))

    response = alt_authenticated_client.post(url)

    assert response.status_code == 204
    assert article.votes.filter(user=alt_user, vote=VoteTypes.DISLIKE).exists() is True


def test_change_like_to_dislike_article(alt_authenticated_client, alt_user, article):
    article.is_published = True
    article.save()
    url_like = reverse('api:articles-add-vote', args=(article.pk, 'like'))
    url_dislike = reverse('api:articles-add-vote', args=(article.pk, 'dislike'))

    alt_authenticated_client.post(url_like)
    response = alt_authenticated_client.post(url_dislike)

    assert response.status_code == 204
    assert article.votes.filter(user=alt_user, vote=VoteTypes.LIKE).exists() is False
    assert article.votes.filter(user=alt_user, vote=VoteTypes.DISLIKE).exists() is True
    assert article.votes.count() == 1


def test_change_dislike_to_like_article(alt_authenticated_client, alt_user, article):
    article.is_published = True
    article.save()
    url_like = reverse('api:articles-add-vote', args=(article.pk, 'like'))
    url_dislike = reverse('api:articles-add-vote', args=(article.pk, 'dislike'))

    alt_authenticated_client.post(url_dislike)
    response = alt_authenticated_client.post(url_like)

    assert response.status_code == 204
    assert article.votes.filter(user=alt_user, vote=VoteTypes.DISLIKE).exists() is False
    assert article.votes.filter(user=alt_user, vote=VoteTypes.LIKE).exists() is True
    assert article.votes.count() == 1


def test_unvote_article(alt_authenticated_client, alt_user, article):
    article.is_published = True
    article.save()
    vote = VoteTypes.LIKE
    add_vote(article, alt_user, vote)
    url = reverse('api:articles-unvote', args=(article.pk,))

    response = alt_authenticated_client.post(url)

    assert response.status_code == 204
    assert article.votes.filter(user=alt_user, vote=vote).exists() is False
    assert article.votes.count() == 0


def test_false_unvote_article(alt_authenticated_client, alt_user, article):
    article.is_published = True
    article.save()
    url = reverse('api:articles-unvote', args=(article.pk,))

    response = alt_authenticated_client.post(url)

    assert response.status_code == 204
    assert article.votes.filter(user=alt_user).exists() is False
    assert article.votes.count() == 0


def test_unvote_unpublished_article(alt_authenticated_client, alt_user, article):
    url = reverse('api:articles-unvote', args=(article.pk,))

    response = alt_authenticated_client.post(url)

    assert response.status_code == 404
    assert article.votes.filter(user=alt_user).exists() is False
    assert article.votes.count() == 0


def test_duplicated_like(alt_authenticated_client, alt_user, article):
    article.is_published = True
    article.save()
    url = reverse('api:articles-add-vote', args=(article.pk, 'like'))

    alt_authenticated_client.post(url)
    response = alt_authenticated_client.post(url)

    assert response.status_code == 204
    assert article.votes.filter(user=alt_user, vote=VoteTypes.LIKE).exists() is True
    assert article.votes.count() == 1


def test_duplicated_dislike(alt_authenticated_client, alt_user, article):
    article.is_published = True
    article.save()
    url = reverse('api:articles-add-vote', args=(article.pk, 'dislike'))

    alt_authenticated_client.post(url)
    response = alt_authenticated_client.post(url)

    assert response.status_code == 204
    assert article.votes.filter(user=alt_user, vote=VoteTypes.DISLIKE).exists() is True
    assert article.votes.count() == 1


def test_duplicated_unvote(alt_authenticated_client, alt_user, article):
    article.is_published = True
    article.save()
    vote = VoteTypes.LIKE
    add_vote(article, alt_user, vote)
    url = reverse('api:articles-unvote', args=(article.pk,))

    alt_authenticated_client.post(url)
    response = alt_authenticated_client.post(url)

    assert response.status_code == 204
    assert article.votes.filter(user=alt_user).exists() is False
    assert article.votes.count() == 0


def test_unpublished_article_favorite(user, authenticated_client, article):
    """Tests unpublished article favoriting."""
    favorite_url = reverse('api:articles-favorite', args=(article.pk,))

    fav_response_unpublished = authenticated_client.post(favorite_url)

    assert fav_response_unpublished.status_code == 404
    assert user.favorite_articles.filter(article=article).exists() is False
    assert user.favorite_articles.count() == 0
    assert FavoriteArticle.objects.count() == 0


def test_unpublished_article_unfavorite(user, authenticated_client, article):
    """Tests unpublished article unfavoriting."""
    favorite_url = reverse('api:articles-favorite', args=(article.pk,))

    unfav_response_unpublished = authenticated_client.delete(favorite_url)

    assert unfav_response_unpublished.status_code == 404
    assert user.favorite_articles.filter(article=article).exists() is False
    assert user.favorite_articles.count() == 0
    assert FavoriteArticle.objects.count() == 0


def test_published_article_favorite(user, authenticated_client, article):
    """Tests published article favoriting."""
    article.is_published = True
    article.save()
    favorite_url = reverse('api:articles-favorite', args=(article.pk,))

    fav_response_published = authenticated_client.post(favorite_url)

    assert fav_response_published.status_code == 201
    assert fav_response_published.data['is_favorited'] is True
    assert user.favorite_articles.filter(article=article).exists() is True
    assert user.favorite_articles.count() == 1
    assert FavoriteArticle.objects.count() == 1

    fav_response_published_duplicate = authenticated_client.post(favorite_url)

    assert fav_response_published_duplicate.status_code == 400
    assert user.favorite_articles.filter(article=article).exists() is True
    assert user.favorite_articles.count() == 1
    assert FavoriteArticle.objects.count() == 1


def test_published_article_unfavorite(user, authenticated_client, article):
    """Tests published article unfavoriting."""
    article.is_published = True
    article.save()
    fav_article = FavoriteArticle.objects.create(user=user, article=article)
    user.favorite_articles.add(fav_article)
    favorite_url = reverse('api:articles-favorite', args=(article.pk,))

    unfav_response_published = authenticated_client.delete(favorite_url)

    assert unfav_response_published.status_code == 200
    assert unfav_response_published.data['is_favorited'] is False
    assert user.favorite_articles.filter(article=article).exists() is False
    assert user.favorite_articles.count() == 0
    assert FavoriteArticle.objects.count() == 0

    unfav_response_published_duplicated = authenticated_client.delete(favorite_url)
    assert unfav_response_published_duplicated.status_code == 400
    assert user.favorite_articles.filter(article=article).exists() is False
    assert user.favorite_articles.count() == 0
    assert FavoriteArticle.objects.count() == 0


def test_published_article_false_unfavorite(user, authenticated_client, article):
    """Tests published article unfavoriting."""
    article.is_published = True
    article.save()
    favorite_url = reverse('api:articles-favorite', args=(article.pk,))

    unfav_response_published = authenticated_client.delete(favorite_url)

    assert unfav_response_published.status_code == 400
    assert user.favorite_articles.filter(article=article).exists() is False
    assert user.favorite_articles.count() == 0
    assert FavoriteArticle.objects.count() == 0
