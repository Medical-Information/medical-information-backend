from django.contrib import admin

from mailings.models import TopArticle


@admin.register(TopArticle)
class TopArticleAdmin(admin.ModelAdmin):
    list_display = (
        'article',
        'article_author',
    )

    def get_queryset(self, request):
        return TopArticle.objects.select_related('article', 'article__author')

    @admin.display()
    def article_author(self, obj):
        return obj.article.author
