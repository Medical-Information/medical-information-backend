from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

class UUIDMixin(models.Model):
    class Meta:
        abstract = True

    pk = models.UUIDField(
        _('id'),
        name='id',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

class TimeStampedMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('modified_at'), auto_now=True)

class Article(UUIDMixin, TimeStampedMixin, models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)
    reading_time = models.IntegerField(null=True, blank=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    source_name = models.CharField(max_length=255, null=True, blank=True)
    source_link = models.TextField(max_length=2047, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tags')
    views_count = models.IntegerField(default=0, editable=False)
    likes = models.ManyToManyField('Likes')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def calculate_reading_time(self):
        words_per_minute = 200
        words = len(self.text.split())
        minutes = words / words_per_minute
        return int(minutes)    

    def increment_views_count(self):
        self.views_count += 1
        self.save()

    def get_likes_count(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        if not self.reading_time and self.text:
            self.reading_time = self.calculate_reading_time()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']
