# Generated by Django 4.2.2 on 2023-07-07 08:27
import uuid
from typing import Any, List

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies: List[Any] = []

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('image', models.ImageField(upload_to='images/')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('text', models.TextField(verbose_name='text')),
                (
                    'source_name',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name='source name',
                    ),
                ),
                (
                    'source_link',
                    models.URLField(
                        blank=True,
                        max_length=2047,
                        null=True,
                        verbose_name='source link',
                    ),
                ),
                (
                    'is_published',
                    models.BooleanField(default=False, verbose_name='is published'),
                ),
                (
                    'views_count',
                    models.IntegerField(default=0, editable=False, verbose_name='views'),
                ),
            ],
            options={
                'verbose_name': 'article',
                'verbose_name_plural': 'articles',
                'ordering': ['-created_at'],
            },
        ),
    ]
