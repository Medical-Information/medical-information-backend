from django.db import models


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomIdMixin(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True