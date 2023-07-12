from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from likes.managers import LikeDislikeManager

User = get_user_model()


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, _('Dislike')),
        (LIKE, _('Like')),
    )
    object_id = models.UUIDField()
    objects = LikeDislikeManager()
    vote = models.SmallIntegerField(verbose_name=_('Vote'),
                                    choices=VOTES,
                                    )
    user = models.ForeignKey(User,
                             verbose_name=_('User'),
                             related_name='likes',
                             on_delete=models.CASCADE,
                             )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
