import django_filters

from articles.models import Article, Tag


class ArticleFilter(django_filters.FilterSet):
    is_favorited = django_filters.BooleanFilter()
    text = django_filters.CharFilter(lookup_expr='icontains')
    tags = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        method='filter_tags',
    )

    class Meta:
        model = Article
        fields = ('text',)

    def filter_tags(self, queryset, name, value):  # noqa: WPS122
        if not value:
            return queryset
        tags = set()
        for tag in value:
            if tag not in tags:
                tags = tags.union(tag.get_descendants(include_self=True))
        return queryset.filter(tags__in=tags).distinct()
