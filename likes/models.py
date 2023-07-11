from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()


class Like(models.Model):
    object_id = models.UUIDField()
    user = models.ForeignKey(User,
                             related_name='likes',
                             on_delete=models.CASCADE,
                             )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
