from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

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


class TagForm(ModelForm):
    """Форма модели Tag. Нужна для проверки дублирования
    в родительских и дочерних тегах.
    """

    def check_tags_matches(self, instance):
        for parent in instance.parents.all():
            if parent in instance.children.all():
                return False, parent.name
        return True, None

    def clean(self):
        ok = False
        with transaction.atomic(savepoint=True, durable=False):
            ok, double = self.check_tags_matches(self.save(commit=True))
            transaction.set_rollback(True)
        if not ok:
            raise ValidationError(
                _('The tag %(double)s cannot be parent and child') % {'double': double},
            )
        return super().clean()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Отображение модели Tag в админ-панели."""

    form = TagForm

    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = (
        ('parents', admin.RelatedOnlyFieldListFilter),
        ('children', admin.RelatedOnlyFieldListFilter),
    )
    list_display = (
        'name',
        'slug',
    )
    list_display_links = (
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
