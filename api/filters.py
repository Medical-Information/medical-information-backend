import uuid

import django_filters

from articles.models import Article, Tag


class ArticleFilter(django_filters.FilterSet):
    is_favorited = django_filters.BooleanFilter(label='Статья в избранном')
    tags = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        method='filter_tags',
        label='Статьи по указанным тегам',
    )
    tags_exclude = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        method='filter_tags_exclude',
        label='Статьи без указанных тегов',
    )

    class Meta:
        model = Article
        fields = ()

    @staticmethod
    def _get_tags_with_children(tags):
        """Формирует набор тегов (выбранные и их потомки) для фильтров по тегам."""
        unique_tags = set()
        for tag in tags:
            if tag not in unique_tags:
                unique_tags = unique_tags.union(tag.get_descendants(include_self=True))
        return unique_tags

    def filter_tags(self, queryset, name, value: list[uuid.UUID]):  # noqa: WPS122
        """Фильтрует articles, выбирая статьи с указанными тегами."""
        if not value:
            return queryset
        return queryset.filter(
            tags__in=ArticleFilter._get_tags_with_children(value),
        ).distinct()

    def filter_tags_exclude(  # noqa: WPS122
        self,
        queryset,
        name,
        value: list[uuid.UUID],
    ):
        """Фильтрует articles, исключая статьи с указанными тегами."""
        if not value:
            return queryset
        return queryset.exclude(
            tags__in=ArticleFilter._get_tags_with_children(value),
        ).distinct()
