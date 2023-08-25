from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from likes.models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'vote',
        'content_type',
        'content_object',
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return Vote.objects.select_related('user', 'content_type').prefetch_related(
            'content_object',
        )
