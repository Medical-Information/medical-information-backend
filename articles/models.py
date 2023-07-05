from django.conf import settings
from django.db import models

from core.models import TimeStampedMixin, UUIDMixin

User = settings.AUTH_USER_MODEL


class Article(UUIDMixin, TimeStampedMixin):
    class Meta:
        ordering = ['-created_at']

    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)
    text = models.TextField()
    source_name = models.CharField(max_length=255, null=True, blank=True)
    source_link = models.URLField(max_length=2047, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField('Tags')
    likes = models.ManyToManyField('Likes')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.reading_time and self.text:
            self.reading_time = self.calculate_reading_time()
        super().save(*args, **kwargs)

    def calculate_reading_time(self):
        words = len(self.text.split())
        minutes = words / 200
        return int(minutes)

    def increment_views_count(self):
        self.views_count += 1
        self.save()

    def get_likes_count(self):
        return self.likes.count()
