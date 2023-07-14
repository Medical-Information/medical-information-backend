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
        tags = self.request.query_params.getlist('tags')
        for tag in tags:
            queryset = queryset.filter(tags__id=tag)
        return queryset
