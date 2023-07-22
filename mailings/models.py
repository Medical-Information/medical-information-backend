from django.db import models
from django.utils.translation import gettext_lazy as _

from articles.models import Article


class TopArticles(models.Model):
    articles = models.ForeignKey(
        Article,
        verbose_name=_('Article'),
        related_name='articles',
        on_delete=models.CASCADE,
    )
