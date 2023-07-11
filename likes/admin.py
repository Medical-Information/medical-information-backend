from django.contrib import admin

from likes.models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'content_type',
        'object_id',
    )
