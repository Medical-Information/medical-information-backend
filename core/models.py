import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)


class UUIDMixin(models.Model):
    class Meta:
        abstract = True

    pk = models.UUIDField(
        _('id'),
        name='id',
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )
