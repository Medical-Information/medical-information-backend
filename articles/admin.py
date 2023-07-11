from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from articles.models import Article, FavoriteArticle, Tag


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
    search_fields = ('author__email', 'title')


class TagForm(ModelForm):
    """Форма модели Tag. Нужна для проверки дублирования
    в родительских и дочерних тегах.
    """

    def check_looping_tags(self, instance):
        """Проверяет на отсутсиве закольцованности тегов,
        если находит, то сообщает имена закольцовывающих тегов."""

        def find_relatives(relation, relatives):
            list_relatives = set()
            for relative in relatives:
                list_relatives = list_relatives.union(getattr(relative, relation).all())
            return list_relatives

        parents = set(instance.parents.all())
        new_parents = parents.copy()
        children = set(instance.children.all())
        new_children = children.copy()
        while True:
            doubles = new_children.intersection(parents)
            doubles = doubles.union(new_parents.intersection(children))
            if len(doubles) > 0:
                doubles = ', '.join(double.name for double in doubles)
                return False, doubles
            parents = parents.union(new_parents)
            children = children.union(new_children)
            new_parents = find_relatives('parents', new_parents)
            new_children = find_relatives('children', new_children)
            if len(new_parents) + len(new_children) == 0:
                break
        return True, None

    def clean(self):
        ok = False
        with transaction.atomic(savepoint=True, durable=False):
            ok, doubles = self.check_looping_tags(self.save(commit=True))
            transaction.set_rollback(True)
        if not ok:
            raise ValidationError(
                _('A tag or tags: %(dbl)s - breaks the hierarchy') % {'dbl': doubles},
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


@admin.register(FavoriteArticle)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'article', 'user')
    list_filter = ('article', 'user')
    search_fields = ('user__email', 'article__title')
    autocomplete_fields = ('article', 'user')
