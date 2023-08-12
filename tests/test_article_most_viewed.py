import itertools
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker

from articles.models import Article, Viewer

User = get_user_model()

pytestmark = pytest.mark.django_db


def test_viewer_created_authenticated(alt_authenticated_client, article, alt_user):
    article.is_published = True
    article.save()
    url = reverse('api:articles-detail', args=(article.id,))

    response = alt_authenticated_client.get(url)

    article.refresh_from_db()
    assert response.status_code == 200
    assert response.data['id'] == str(article.id)
    assert Viewer.objects.count() == 1
    assert Viewer.objects.filter(user=alt_user, ipaddress__isnull=True).exists() is True
    assert Viewer.objects.filter(user=alt_user, ipaddress__isnull=True).count() == 1
    assert article.viewers.count() == 1
    assert article.viewers.filter(user=alt_user, ipaddress__isnull=True).exists() is True
    assert article.viewers.filter(user=alt_user, ipaddress__isnull=True).count() == 1


def test_viewer_created_anonymous(client, article):
    article.is_published = True
    article.save()
    url = reverse('api:articles-detail', args=(article.id,))

    response = client.get(url)

    article.refresh_from_db()
    assert response.status_code == 200
    assert response.data['id'] == str(article.id)
    assert Viewer.objects.count() == 1
    assert (
        Viewer.objects.filter(user__isnull=True, ipaddress__isnull=False).exists()
        is True
    )
    assert Viewer.objects.filter(user__isnull=True, ipaddress__isnull=False).count() == 1
    assert article.viewers.count() == 1
    assert (
        article.viewers.filter(user__isnull=True, ipaddress__isnull=False).exists()
        is True
    )
    assert (
        article.viewers.filter(user__isnull=True, ipaddress__isnull=False).count() == 1
    )


def test_most_viewed_article_not_found(client):
    """No viewers exist, no published articles."""
    url = reverse('api:articles-the-most-popular')

    response = client.get(url)

    assert response.status_code == 404


def test_most_viewed_article_no_viewers(client, article):
    """No viewers exist, defined by creation time."""
    article.is_published = True
    article.save()
    url = reverse('api:articles-the-most-popular')

    response = client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == str(article.pk)


def test_most_viewed_article_anonymous(client, article, faker):
    article.is_published = True
    article.save()
    url = reverse('api:articles-the-most-popular')

    alt_article = baker.make(Article)
    alt_article.is_published = True
    alt_article.save()

    viewers_count_to_create = 15
    anonymous_viewers = baker.make(
        Viewer,
        ipaddress=faker.ipv4,
        user=None,
        _quantity=viewers_count_to_create,
    )

    assert Viewer.objects.count() == viewers_count_to_create

    article.viewers.set(anonymous_viewers[:10])
    alt_article.viewers.set(anonymous_viewers[10:])

    assert article.viewers.count() == 10
    assert alt_article.viewers.count() == 5

    response = client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == str(article.pk)


def test_most_viewed_article_authenticated(client, article):
    article.is_published = True
    article.save()
    url = reverse('api:articles-the-most-popular')

    alt_article = baker.make(Article)
    alt_article.is_published = True
    alt_article.save()

    viewers_count_to_create = 15
    users = baker.make(User, _quantity=viewers_count_to_create)
    viewers = baker.make(
        Viewer,
        ipaddress=None,
        user=itertools.cycle(users),
        _quantity=viewers_count_to_create,
    )

    assert Viewer.objects.count() == viewers_count_to_create

    article.viewers.set(viewers[:10])
    alt_article.viewers.set(viewers[10:])

    assert article.viewers.count() == 10
    assert alt_article.viewers.count() == 5

    response = client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == str(article.pk)


def test_most_viewed_same_viewer_count(client, article):
    """Most viewed article defined by creation time."""
    article.is_published = True
    article.save()
    url = reverse('api:articles-the-most-popular')

    alt_article = baker.make(Article)
    alt_article.is_published = True
    alt_article.created_at = article.created_at - timedelta(minutes=10)
    alt_article.save()

    viewers_count_to_create = 20
    users = baker.make(User, _quantity=viewers_count_to_create)
    viewers = baker.make(
        Viewer,
        ipaddress=None,
        user=itertools.cycle(users),
        _quantity=viewers_count_to_create,
    )

    assert Viewer.objects.count() == viewers_count_to_create

    article.viewers.set(viewers[:10])
    alt_article.viewers.set(viewers[10:])

    assert article.viewers.count() == 10
    assert alt_article.viewers.count() == 10

    response = client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == str(article.pk)
