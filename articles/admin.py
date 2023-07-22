from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import ModelForm
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter

from articles.models import Article, FavoriteArticle, Tag


class ArticleForm(ModelForm):
    annotation = forms.CharField(widget=forms.Textarea)

    def check_for_sub_tags(self, instance):
        tags = sorted(instance.tags.all(), key=lambda tag: tag.level)
        while len(tags) > 0:
            tag = tags.pop()
            ancestors = tag.get_ancestors(include_self=False)
            intersec_tags = set(tags).intersection(ancestors)
            if len(intersec_tags) > 0:
                related_tags = ', '.join(r_tag.name for r_tag in intersec_tags)
                related_tags += f', {tag.name}'
                return False, related_tags

        return True, None

    def clean(self):
        ok = False
        with transaction.atomic(savepoint=True, durable=False):
            ok, related_tags = self.check_for_sub_tags(self.save(commit=True))
            transaction.set_rollback(True)
        if not ok:
            raise ValidationError(
                _("You can't assign related tags <%(reltags)s> to content!")
                % {'reltags': related_tags},
            )
        return super().clean()


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
                    ('text', 'image'),
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
    list_filter = ('author', 'is_published', ('tags', TreeRelatedFieldListFilter))
    search_fields = ('author__email', 'title')
    filter_horizontal = ('tags',)
    readonly_fields = (
        'created_at',
        'updated_at',
        'views_count',
    )


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
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'article', 'user')
    list_filter = ('article', 'user')
    search_fields = ('user__email', 'article__title')
    autocomplete_fields = ('article', 'user')
