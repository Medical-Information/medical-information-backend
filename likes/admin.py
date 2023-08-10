from django.contrib import admin

from likes.models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'vote',
        'content_type',
        'content_object',
    )
