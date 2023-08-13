import pytest
from django.urls import reverse
from model_bakery import baker

from articles.models import Comment

mark = pytest.mark.django_db


def test_comment_list(article, authenticated_client):
    article.is_published = True
    article.save()
    url = reverse('api:comments-list', args=(article.pk,))
    comments_quantity = 25
    baker.make(Comment, article=article, _quantity=comments_quantity)

    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == comments_quantity
    assert article.comments.count() == comments_quantity
    assert Comment.objects.count() == comments_quantity


def test_comment_creation(article, authenticated_client, faker, user):
    article.is_published = True
    article.save()
    url = reverse('api:comments-list', args=(article.pk,))
    comment_data = {
        'text': faker.paragraph(),
    }

    response = authenticated_client.post(url, comment_data, format='json')

    assert response.status_code == 201
    assert response.data['author']['id'] == str(user.pk)
    assert response.data['text'] == comment_data['text']
    assert article.comments.count() == 1
    assert article.comments.get(author=user) is not None


def test_comment_get(article, authenticated_client, alt_user, faker):
    article.is_published = True
    article.save()
    text = faker.paragraph()
    comment = Comment.objects.create(author=alt_user, article=article, text=text)
    url = reverse('api:comments-detail', args=(article.pk, comment.pk))

    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == str(comment.pk)
    assert response.data['text'] == text
    assert response.data['author']['id'] == str(alt_user.pk)


def test_comment_alteration_put_method(article, authenticated_client, user, faker):
    article.is_published = True
    article.save()
    text = faker.paragraph()
    comment = Comment.objects.create(author=user, article=article, text=text)
    new_text = faker.paragraph()
    new_comment_data = {
        'text': new_text,
    }
    url = reverse('api:comments-detail', args=(article.pk, comment.pk))

    response = authenticated_client.put(url, new_comment_data, format='json')

    comment.refresh_from_db()
    assert response.status_code == 200
    assert response.data['text'] == new_text
    assert comment.text == new_text


def test_comment_alteration_put_method_not_owner(
    article,
    authenticated_client,
    alt_user,
    faker,
):
    article.is_published = True
    article.save()
    text = faker.paragraph()
    comment = Comment.objects.create(author=alt_user, article=article, text=text)
    new_text = faker.paragraph()
    new_comment_data = {
        'text': new_text,
    }
    url = reverse('api:comments-detail', args=(article.pk, comment.pk))

    response = authenticated_client.put(url, new_comment_data, format='json')

    comment.refresh_from_db()
    assert response.status_code == 403
    assert comment.text == text


def test_comment_alteration_patch_method(article, authenticated_client, user, faker):
    article.is_published = True
    article.save()
    text = faker.paragraph()
    comment = Comment.objects.create(author=user, article=article, text=text)
    new_text = faker.paragraph()
    new_comment_data = {
        'text': new_text,
    }
    url = reverse('api:comments-detail', args=(article.pk, comment.pk))

    response = authenticated_client.patch(url, new_comment_data, format='json')

    comment.refresh_from_db()
    assert response.status_code == 200
    assert response.data['text'] == new_text
    assert comment.text == new_text


def test_comment_alteration_patch_method_not_owner(
    article,
    authenticated_client,
    alt_user,
    faker,
):
    """Попытка изменения комментария другого пользователя."""
    article.is_published = True
    article.save()
    text = faker.paragraph()
    comment = Comment.objects.create(author=alt_user, article=article, text=text)
    new_text = faker.paragraph()
    new_comment_data = {
        'text': new_text,
    }
    url = reverse('api:comments-detail', args=(article.pk, comment.pk))

    response = authenticated_client.patch(url, new_comment_data, format='json')

    comment.refresh_from_db()
    assert response.status_code == 403
    assert comment.text == text


def test_comment_deletion(article, authenticated_client, user, faker):
    """Удаление собственного комментария."""
    article.is_published = True
    article.save()
    text = faker.paragraph()
    comment = Comment.objects.create(author=user, article=article, text=text)
    url = reverse('api:comments-detail', args=(article.pk, comment.pk))

    response = authenticated_client.delete(url)

    assert response.status_code == 200
    assert response.data is not None
    assert response.data['id'] is None
    assert response.data['text'] == comment.text
    assert response.data['author']['id'] == str(user.pk)
    assert 'created_at' in response.data
    assert 'updated_at' in response.data
    assert Comment.objects.filter(pk=comment.pk).exists() is False


def test_comment_deletion_not_owner(article, authenticated_client, alt_user, faker):
    """Попытка удаления комменраия другого пользователя."""
    article.is_published = True
    article.save()
    text = faker.paragraph()
    comment = Comment.objects.create(author=alt_user, article=article, text=text)
    url = reverse('api:comments-detail', args=(article.pk, comment.pk))

    response = authenticated_client.delete(url)

    assert response.status_code == 403
    assert Comment.objects.filter(pk=comment.pk).exists() is True


def test_comment_anonymous_create(article, faker, client):
    article.is_published = True
    article.save()
    url = reverse('api:comments-list', args=(article.pk,))
    comment_data = {
        'text': faker.paragraph(),
    }

    response = client.post(url, comment_data, format='json')

    assert response.status_code == 401
    assert article.comments.count() == 0


def test_comment_anonymous_list(article, client):
    article.is_published = True
    article.save()
    url = reverse('api:comments-list', args=(article.pk,))
    comments_quantity = 25
    baker.make(Comment, article=article, _quantity=comments_quantity)

    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == comments_quantity


def test_comment_anonymous_get(article, faker, alt_user, client):
    article.is_published = True
    article.save()
    text = faker.paragraph()
    comment = Comment.objects.create(author=alt_user, article=article, text=text)
    url = reverse('api:comments-detail', args=(article.pk, comment.pk))

    response = client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == str(comment.pk)
    assert response.data['text'] == text
    assert response.data['author']['id'] == str(alt_user.pk)


def test_comment_anonymous_put(article, faker, user, client):
    article.is_published = True
    article.save()
    text = faker.paragraph()
    comment = Comment.objects.create(author=user, article=article, text=text)
    new_text = faker.paragraph()
    new_comment_data = {
        'text': new_text,
    }
    url = reverse('api:comments-detail', args=(article.pk, comment.pk))

    response = client.put(url, new_comment_data, format='json')

    comment.refresh_from_db()
    assert response.status_code == 401
    assert comment.text == text


def test_comment_anonymous_patch(article, faker, user, client):
    article.is_published = True
    article.save()
    text = faker.paragraph()
    comment = Comment.objects.create(author=user, article=article, text=text)
    new_text = faker.paragraph()
    new_comment_data = {
        'text': new_text,
    }
    url = reverse('api:comments-detail', args=(article.pk, comment.pk))

    response = client.patch(url, new_comment_data, format='json')

    comment.refresh_from_db()
    assert response.status_code == 401
    assert comment.text == text


def test_comment_anonymous_delete(article, faker, alt_user, client):
    article.is_published = True
    article.save()
    text = faker.paragraph()
    comment = Comment.objects.create(author=alt_user, article=article, text=text)
    url = reverse('api:comments-detail', args=(article.pk, comment.pk))

    response = client.delete(url)

    assert response.status_code == 401
    assert Comment.objects.filter(pk=comment.pk).exists() is True
