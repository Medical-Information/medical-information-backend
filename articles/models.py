from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField

from core.models import TimeStampedMixin, UUIDMixin
from likes.models import Vote

User = get_user_model()


class Article(UUIDMixin, TimeStampedMixin):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(_('title'), max_length=255)
    text = models.TextField(_('text'))
    source_name = models.CharField(
        _('source name'),
        max_length=255,
        null=True,
        blank=True,
    )
    source_link = models.URLField(
        _('source link'),
        max_length=2047,
        null=True,
        blank=True,
    )
    is_published = models.BooleanField(_('is published'), default=False)
    views_count = models.IntegerField(_('views'), default=0, editable=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles',
        null=True,
        blank=True,
    )
    tags = TreeManyToManyField(
        'Tag',
        related_name='articles',
        verbose_name=_('tags'),
        blank=True,
    )
    votes = GenericRelation(Vote, related_query_name='articles')

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.votes.likes().count()

    @property
    def dislikes_count(self):
        return self.votes.dislikes().count()

    @property
    def rating(self):
        return self.votes.sum_rating()

    def increment_views_count(self):
        self.views_count += 1
        self.save()


class Tag(UUIDMixin, MPTTModel):
    """Теги."""

    name = models.CharField(
        verbose_name=_('Tag name'),
        max_length=100,
        unique=True,
    )
    parent = TreeForeignKey(
        'self',
        related_name='children',
        verbose_name=_('Parent category'),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        db_index=True,
    )

    class Meta:
        verbose_name_plural = _('Tags')
        verbose_name = _('Tag')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('post-by-category', args=[str(self.slug)])


class FavoriteArticle(UUIDMixin):
    """Избранная статья пользователя (закладка)."""

    user = models.ForeignKey(
        User,
        related_name='favorite_articles',
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        help_text=_('select user'),
    )

    article = models.ForeignKey(
        Article,
        related_name='favorite_articles',
        on_delete=models.CASCADE,
        verbose_name=_('article'),
        help_text=_('select article'),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_unique_favorite',
                fields=['article', 'user'],
            ),
        ]
        verbose_name = _('favorite article')
        verbose_name_plural = _('favorite articles')

    def __str__(self) -> str:
        return f'Избранное (пользователь: {self.user}, статья {self.article})'
