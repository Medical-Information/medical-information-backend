from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.db.models.query import QuerySet

User = get_user_model()


def annotate_user_queryset(user_queryset: QuerySet[User]) -> QuerySet[User]:
    return user_queryset.annotate(
        rating=Coalesce(Sum('articles__votes__vote'), 0),
    ).annotate(publications_amount=Count('articles', distinct=True))
