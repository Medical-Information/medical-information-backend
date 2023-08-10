from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from likes.models import Vote

User = get_user_model()


def add_vote(obj, user, vote_type):
    """Добавляет голос (лайк/дизлайк) пользователя по объекту."""
    obj_type = ContentType.objects.get_for_model(obj)
    vote, is_created = Vote.objects.get_or_create(
        content_type=obj_type,
        object_id=obj.id,
        user=user,
        defaults={'vote': vote_type},
    )
    if not is_created and vote.vote != vote_type:
        vote.vote = vote_type
        vote.save()

    return vote


def remove_vote(obj, user):
    """Удаляет голос (лайк/дизлайк) пользователя по объекту."""
    obj_type = ContentType.objects.get_for_model(obj)
    Vote.objects.filter(
        content_type=obj_type,
        object_id=obj.id,
        user=user,
    ).delete()


def is_object_voted_by_user(obj, user, vote_type=None) -> bool:
    """Проверяет голосовал ли пользователь по объекту."""
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Vote.objects.filter(
        content_type=obj_type,
        object_id=obj.id,
        user=user,
        vote=vote_type,
    )
    return likes.exists()


def get_voters_by_object(obj, vote_group):
    """Возвращает всех пользователей, голосовавших по объекту."""
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        likes__content_type=obj_type,
        likes__object_id=obj.id,
        likes__vote=vote_group,
    )
