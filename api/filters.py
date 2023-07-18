import django_filters

from articles.models import Article, Tag


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = ('text',)

    is_favorited = django_filters.BooleanFilter()
    text = django_filters.CharFilter(lookup_expr='icontains')
    tags = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        method='filter_tags',
    )

    def filter_tags(self, queryset, name, value):  # noqa
        if not value:
            return queryset
        tagsset = set()
        for tag in value:
            if tag not in tagsset:
                tagsset = tagsset.union(tag.get_descendants(include_self=True))
        return queryset.filter(tags__in=tagsset).distinct()
