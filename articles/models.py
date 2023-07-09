from django.conf import settings
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedMixin, UUIDMixin

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
    tags = models.ManyToManyField(
        'Tag',
        related_name='articles',
        verbose_name=_('tags'),
        blank=True,
    )
    # likes = models.ManyToManyField('Users') # noqa

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if not self.reading_time and self.text:
        if self.text:
            self.reading_time = self.calculate_reading_time()
        super().save(*args, **kwargs)

    def calculate_reading_time(self):
        words = len(self.text.split())
        minutes = words / 200
        return int(minutes)

    def increment_views_count(self):
        self.views_count += 1
        self.save()

    def get_likes_count(self):
        return self.likes.count()


class Tag(UUIDMixin):
    """Теги."""

    class Meta:
        ordering = ('name',)
        verbose_name_plural = _('Tags')
        verbose_name = _('Tag')

    name = models.CharField(verbose_name=_('Tag name'), max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    children = models.ManyToManyField(
        'Tag',
        related_name='prnts',
        verbose_name=_('Children'),
        blank=True,
    )
    parents = models.ManyToManyField(
        'Tag',
        related_name='chldrn',
        verbose_name=_('Parents'),
        blank=True,
    )

    def __str__(self) -> str:
        return self.name


@receiver(m2m_changed, sender=Tag.children.through)
def change_parents(action, instance, **kwargs):
    """При удалении тегов-потомков удаляет у потомков родителя."""
    m2m_changed.disconnect(change_children, sender=Tag.parents.through)
    if action == 'post_add':
        for child in instance.children.all():
            child.parents.add(instance)
    elif action == 'pre_remove':
        for child in instance.children.all():
            child.parents.remove(instance)
    m2m_changed.connect(change_children, sender=Tag.parents.through)


@receiver(m2m_changed, sender=Tag.parents.through)
def change_children(action, instance, **kwargs):
    """При удалении тегов-родителей удаляет у родителей потомков."""
    m2m_changed.disconnect(change_parents, sender=Tag.children.through)
    if action == 'post_add':
        for parent in instance.parents.all():
            parent.children.add(instance)
    elif action == 'pre_remove':
        for parent in instance.parents.all():
            parent.children.remove(instance)
    m2m_changed.connect(change_parents, sender=Tag.children.through)
