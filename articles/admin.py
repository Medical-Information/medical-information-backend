from django.contrib import admin

from articles.models import Article, Tag


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'text',
        'source_link',
        'is_published',
        'views_count',
    )
    list_filter = ('author', 'is_published')
    search_fields = ('author',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Отображение модели Tag в админ-панели."""

    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = (
        ('parents', admin.RelatedOnlyFieldListFilter),
        ('children', admin.RelatedOnlyFieldListFilter),
    )
    list_display = (
        'id',
        'name',
        'slug',
    )
    list_display_links = (
        'id',
        'name',
        'slug',
    )
    fields = (
        'name',
        'slug',
        'children',
        'parents',
    )
    filter_horizontal = (
        'children',
        'parents',
    )
