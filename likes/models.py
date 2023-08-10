from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from likes.managers import VoteManager

User = get_user_model()


class VoteTypes(models.IntegerChoices):
    LIKE = 1, _('Like')
    DISLIKE = -1, _('Dislike')


class Vote(models.Model):
    object_id = models.UUIDField()
    objects = VoteManager()
    vote = models.IntegerField(
        verbose_name=_('Vote'),
        choices=VoteTypes.choices,
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        related_name='likes',
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
