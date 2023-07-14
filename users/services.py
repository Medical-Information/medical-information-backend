from django.db.models import Sum

from articles.models import Article
from likes.models import LikeDislike


def rating(user):
    return LikeDislike.objects.filter(
        user=user.id,
    ).aggregate(Sum('vote')).get('vote__sum') or 0


def publications(user):
    return Article.objects.filter(author=user).count()
