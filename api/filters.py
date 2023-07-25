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

    def tags_set(self, tags):
        """Формирует набор тегов (выбранные и их потомки) для фильтров по тегам."""
        tagsset = set()
        for tag in tags:
            if tag not in tagsset:
                tagsset = tagsset.union(tag.get_descendants(include_self=True))
        return tagsset

    def filter_tags(self, queryset, name, value):  # noqa: WPS122
        """Фильтрует aticles, выбирая статьи с указанными тегами."""
        if not value:
            return queryset
        return queryset.filter(tags__in=self.tags_set(value)).distinct()

    def filter_tags_exclude(self, queryset, name, value):  # noqa: WPS122
        """Фильтрует aticles, исключая статьи с указанными тегами."""
        if not value:
            return queryset
        return queryset.exclude(tags__in=self.tags_set(value)).distinct()
