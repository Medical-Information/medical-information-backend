from rest_framework.filters import SearchFilter


class ArticleTextSearchFilter(SearchFilter):
    search_param = 'text'
