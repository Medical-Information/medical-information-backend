from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.db.models.query import QuerySet


def annotate_user_queryset(user_queryset: QuerySet) -> QuerySet:
    return (
        user_queryset.annotate(rating=Coalesce(Sum('likes__vote'), 0))
        .annotate(publications_amount=Count('articles', distinct=True))
        .all()
    )
