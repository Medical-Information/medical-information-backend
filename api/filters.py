import django_filters

from articles.models import Article, Tag


class ArticleFilter(django_filters.FilterSet):
    is_favorited = django_filters.BooleanFilter()
    text = django_filters.CharFilter(lookup_expr='icontains')
    tags = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        method='filter_tags',
    )
    tags_exclude = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        method='filter_tags_exclude',
    )

    class Meta:
        model = Article
        fields = ('text',)

    def get_tags_with_children(self, tags):
        """Формирует набор тегов (выбранные и их потомки) для фильтров по тегам."""
        unique_tags = set()
        for tag in tags:
            if tag not in unique_tags:
                unique_tags = unique_tags.union(tag.get_descendants(include_self=True))
        return unique_tags

    def filter_tags(self, queryset, name, value):  # noqa: WPS122
        """Фильтрует articles, выбирая статьи с указанными тегами."""
        if not value:
            return queryset
        return queryset.filter(tags__in=self.get_tags_with_children(value)).distinct()

    def filter_tags_exclude(self, queryset, name, value):  # noqa: WPS122
        """Фильтрует articles, исключая статьи с указанными тегами."""
        if not value:
            return queryset
        return queryset.exclude(tags__in=self.get_tags_with_children(value)).distinct()
