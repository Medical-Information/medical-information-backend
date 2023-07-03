from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
import uuid

class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)
    reading_time = models.IntegerField(null=True, blank=True)
    text = models.TextField()
    author = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    source_name = models.CharField(max_length=255, null=True, blank=True)
    source_link = models.CharField(max_length=255, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tags')
    views_count = models.IntegerField(default=0, editable=False)
    likes = models.ManyToManyField('Likes')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def increment_views_count(self):
        self.views_count += 1
        self.save()

    def get_likes_count(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_at']
