from typing import Any

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count
from django.db.models.query import QuerySet
from django.forms import ModelForm
from django.http.request import HttpRequest
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from mdeditor.widgets import MDEditorWidget
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter

from articles.models import Article, Comment, FavoriteArticle, Tag, Viewer


class ArticleForm(ModelForm):
    annotation = forms.CharField(widget=MDEditorWidget)

    def check_for_sub_tags(self, tags):
        """Проверяет, что среди переданных тегов нет связанных предков и потомков."""
        tags = sorted(tags, key=lambda tag: tag.level)
        while len(tags) > 0:
            tag = tags.pop()
            ancestors = tag.get_ancestors(include_self=False)
            tags_intersection = set(tags).intersection(ancestors)
            if len(tags_intersection) > 0:
                related_tags = ', '.join(r_tag.name for r_tag in tags_intersection)
                related_tags += f', {tag.name}'
                return False, related_tags

        return True, None

    def clean(self):
        """Вызывает проверку связанных тегов, если найдены выбрасывает исключение."""
        tags = self.cleaned_data.get('tags')
        ok, related_tags = self.check_for_sub_tags(tags)
        if not ok:
            raise ValidationError(
                _("You can't assign related tags <%(related_tags)s> to content!")
                % {'related_tags': related_tags},
            )
        return self.cleaned_data


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm
    fieldsets = [
        (
            None,
            {
                'fields': [
                    'title',
                    'annotation',
                    'text',
                    'image',
                    ('author', 'is_published'),
                    ('source_name', 'source_link'),
                    'tags',
                ],
            },
        ),
        (
            _('Statistics'),
            {
                'fields': [('created_at', 'updated_at', 'views_count')],
            },
        ),
    ]

    list_display = (
        'title',
        'author',
        'source_link',
        'is_published',
        'views_count',
        'created_at',
        'updated_at',
    )
    list_select_related = ('author',)
    list_filter = ('is_published', ('tags', TreeRelatedFieldListFilter))
    search_fields = ('author__email', 'title')
    filter_horizontal = ('tags',)
    readonly_fields = (
        'created_at',
        'updated_at',
        'views_count',
    )
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget},
    }

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(views_count=Count('viewers'))
        return queryset

    def views_count(self, obj):
        return obj.views_count


@admin.register(Tag)
class TagAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
    )
    search_fields = ('title',)
    mptt_level_indent = 35

    def tree_actions(self, instance):
        try:
            url = instance.get_absolute_url()
        except Exception:  # noqa: B902
            url = ''

        return format_html(
            '<div class="tree-node" data-pk="{inst}" data-level="{lvl}"'
            + ' data-url="{url}"></div>',
            inst=instance.pk,
            lvl=instance._mpttfield('level'),
            url=url,
        )


@admin.register(FavoriteArticle)
class FavoriteArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'article', 'user')
    list_filter = ('article', 'user')
    search_fields = ('user__email', 'article__title')
    autocomplete_fields = ('article', 'user')


@admin.register(Viewer)
class ViewerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ipaddress', 'user')
    search_fields = ('user__email', 'article__title')
    autocomplete_fields = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'article',
        'text',
    )
    list_select_related = ('author',)
    list_filter = ('article', 'author')
    search_fields = ('text',)
