from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from articles.models import Article, Tag


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
