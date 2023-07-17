import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField

from core.models import TimeStampedMixin, UUIDMixin
from likes.models import LikeDislike

User = settings.AUTH_USER_MODEL


class Article(UUIDMixin, TimeStampedMixin):
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('article')
        verbose_name_plural = _('articles')

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tags = TreeManyToManyField(
        'Tag',
        related_name='articles',
        verbose_name=_('tags'),
        blank=True,
    )
    votes = GenericRelation(LikeDislike, related_query_name='articles')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if not self.reading_time and self.text:
        if self.text:
            self.reading_time = self.calculate_reading_time()
        super().save(*args, **kwargs)

    @property
    def likes_count(self):
        return self.votes.likes().count()

    @property
    def dislikes_count(self):
        return self.votes.dislikes().count()

    @property
    def rating(self):
        return self.votes.sum_rating()

    def calculate_reading_time(self):
        words = len(self.text.split())
        minutes = words / 200
        return int(minutes)

    def increment_views_count(self):
        self.views_count += 1
        self.save()


class Tag(MPTTModel):
    """Теги."""

    class Meta:
        verbose_name_plural = _('Tags')
        verbose_name = _('Tag')

    class MPTTMeta:
        order_insertion_by = ['name']

    pk = models.UUIDField(
        _('id'),
        name='id',
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )
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

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('post-by-category', args=[str(self.slug)])


class FavoriteArticle(UUIDMixin):
    """Избранная статья пользователя (закладка)."""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_unique_favorite',
                fields=['article', 'user'],
            ),
        ]
        verbose_name = _('favorite article')
        verbose_name_plural = _('favorite articles')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        help_text=_('select user'),
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name=_('article'),
        help_text=_('select article'),
    )

    def __str__(self) -> str:
        return f'Избранное (пользователь: {self.user}, статья {self.article})'
