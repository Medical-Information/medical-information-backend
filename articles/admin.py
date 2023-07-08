from django.contrib import admin

from articles.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'text', 'source_link', 'is_published', 'views_count',
    )
    list_filter = ('author', 'is_published')
    search_fields = ('author',)
