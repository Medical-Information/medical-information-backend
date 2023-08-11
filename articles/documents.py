from django_opensearch_dsl import Document
from django_opensearch_dsl.registries import registry

from articles.models import Article


@registry.register_document
class ArticleDocument(Document):
    class Index:
        name = 'articles'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }
        auto_refresh = True

    class Django:
        model = Article
        fields = [
            'text',
        ]
        queryset_pagination = 5000
