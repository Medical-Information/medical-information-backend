import django_filters

from articles.models import Article


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = ('text',)

    is_favorited = django_filters.BooleanFilter()
    text = django_filters.CharFilter(lookup_expr='icontains')
