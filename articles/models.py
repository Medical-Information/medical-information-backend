from django.contrib.auth.models import User
from django.db import models

from mixins.models import TimeStampedMixin, UUIDMixin

class Article(UUIDMixin, TimeStampedMixin):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    source_name = models.CharField(max_length=255, null=True, blank=True)
    source_link = models.URLField(max_length=2047, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tags')
    views_count = models.IntegerField(default=0, editable=False)
    likes = models.ManyToManyField('Likes')

    def __str__(self):
        return self.title

    def calculate_reading_time(self):
        words = len(self.text.split())
        minutes = words / 200
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
