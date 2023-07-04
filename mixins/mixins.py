import uuid

from django.db import models
from django.utils import timezone


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
