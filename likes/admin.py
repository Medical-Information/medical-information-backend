from django.contrib import admin

from likes.models import LikeDislike


@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'vote',
        'content_type',
        'content_object',
    )
