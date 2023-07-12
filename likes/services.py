from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from likes.models import LikeDislike

User = get_user_model()


def add_likedislike(obj, user, vote_type):
    """Adds a like/dislike to an object"""
    obj_type = ContentType.objects.get_for_model(obj)
    likedislike, is_created = LikeDislike.objects.get_or_create(
        content_type=obj_type,
        object_id=obj.id,
        user=user,
        defaults={'vote': vote_type},
    )
    if not is_created and likedislike.vote != vote_type:
        likedislike.vote = vote_type
        likedislike.save()

    return likedislike


def remove_vote(obj, user):
    """Removes the user's voice from obj"""
    obj_type = ContentType.objects.get_for_model(obj)
    LikeDislike.objects.filter(content_type=obj_type,
                               object_id=obj.id,
                               user=user).delete()


def is_group(obj, user, vote_type=None) -> bool:
    """Checks if the user has liked the obj.
    """
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = LikeDislike.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user, vote=vote_type)
    return likes.exists()


def get_group(obj, vote_group):
    """Gets all users who voted for obj.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        likes__content_type=obj_type,
        likes__object_id=obj.id,
        likes__vote=vote_group,
    )
