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


@receiver(m2m_changed, sender=Article.tags.through)
def changing_tags_set(action, instance, pk_set, **kwargs):
    """Добавляет предков тега к статье при добавлении тега,
    и удаляет потомков при удалении тега, оставляя тех,
    что имеют в данной статье других предков."""

    m2m_changed.disconnect(changing_tags_set, sender=Article.tags.through)
    if action == 'post_add':
        add_upper_tags(instance, pk_set)
    elif action == 'post_remove':
        remove_lower_tags(instance, pk_set)
    m2m_changed.connect(changing_tags_set, sender=Article.tags.through)


def add_upper_tags(instance, pk_set):
    """Добавляет предков тега к статье при добавлении тега."""

    def find_parents(child):
        parents = set()
        for parent in child.parents.all():
            parents.add(parent)
            parents = parents.union(find_parents(parent))
        return parents

    add_tags = set()
    for pk in pk_set:
        tag = Tag.objects.get(pk=pk)
        add_tags = add_tags.union(find_parents(tag))
        for parent in tag.parents.all():
            add_tags.add(parent)
    for tag in add_tags:
        instance.tags.add(tag)


def remove_lower_tags(instance, pk_set):
    """Удаляет потомков при удалении тега, оставляя тех,
    что имеют в данной статье других предков.
    """

    def find_children(parent):
        children = set()
        for child in parent.children.all():
            children.add(child)
            children = children.union(find_children(child))
        return children

    tags_to_del = set()
    tags_not_del = set(instance.tags.all())
    saved_tags = set()
    for pk in pk_set:
        tag_d = Tag.objects.get(pk=pk)
        tags_to_del = tags_to_del.union(find_children(tag_d))
    tags_not_del = tags_not_del - tags_to_del
    for tag_s in tags_not_del:
        saved_tags = saved_tags.union(find_children(tag_s))
    for del_tag in tags_to_del - saved_tags:
        instance.tags.remove(del_tag)


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
def change_parents(action, instance, pk_set, **kwargs):
    """При добавлении/удалении тегов-потомков добавляет/удаляет у потомков родителя."""
    sym_relatives(change_parents, 'children', action, instance, pk_set)


@receiver(m2m_changed, sender=Tag.parents.through)
def change_children(action, instance, pk_set, **kwargs):
    """При добавлении/удалении тегов-родителей добавляет/удаляет у родителей потомков."""
    sym_relatives(change_children, 'parents', action, instance, pk_set)


def sym_relatives(func, field, action, instance, pk_set):
    """Добавляет/удаляет связи тегов по заданным параметрам."""

    sender = Tag.parents.through if field == 'parents' else Tag.children.through
    m2m_changed.disconnect(func, sender=sender)
    if action == 'post_add':
        for pk in pk_set:
            relative = Tag.objects.get(pk=pk)
            getattr(relative, field).add(instance)
    elif action == 'post_remove':
        for pk in pk_set:
            relative = Tag.objects.get(pk=pk)
            getattr(relative, field).remove(instance)
    m2m_changed.connect(func, sender=sender)
