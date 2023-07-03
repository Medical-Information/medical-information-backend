import uuid

from django.db import models
from django.utils import timezone


class TimeStampedMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class UUIDMixin(models.Model):
    class Meta:
        abstract = True

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
