from django.db.models import Sum

from articles.models import Article
from likes.models import LikeDislike


def get_rating(user) -> int:
    return (
        LikeDislike.objects.filter(
            user=user.id,
        )
        .aggregate(Sum('vote'))
        .get('vote__sum', 0)
    )


def get_publications_amount(user) -> int:
    return Article.objects.filter(author=user).count()
