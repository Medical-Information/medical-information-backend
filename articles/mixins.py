from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class UUIDMixin(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(
        _('id'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

class TimeStampedMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('modified_at'), auto_now=True)
