# Generated by Django 4.2.2 on 2023-07-21 08:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LikeDislike',
        ),
    ]