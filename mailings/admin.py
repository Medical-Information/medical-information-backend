from django.contrib import admin

from mailings.models import TopArticles


@admin.register(TopArticles)
class TopArticlesAdmin(admin.ModelAdmin):
    list_display = (
        'articles',
    )
