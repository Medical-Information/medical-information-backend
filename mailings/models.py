from django.db import models
from django.utils.translation import gettext_lazy as _

from articles.models import Article


class TopArticle(models.Model):
    article = models.OneToOneField(
        Article,
        verbose_name=_('TopArticle'),
        related_name='top_article',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('TopArticle')
        verbose_name_plural = _('TopArticles')
        ordering = ('-pk',)

    def __str__(self):
        return f'TopArticle({self.article})'
