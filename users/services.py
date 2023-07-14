from django.db.models import Sum

from articles.models import Article
from likes.models import LikeDislike


def rating(user):
    rating = LikeDislike.objects.filter(
        user=user.id,
    ).aggregate(Sum('vote')).get('vote__sum') or 0
    return rating


def publications(user):
    articles_count = Article.objects.filter(
        author=user,
    ).count()
    return articles_count
