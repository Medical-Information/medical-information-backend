# Generated by Django 4.2.2 on 2023-07-10 10:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='object_id',
            field=models.UUIDField(),
        ),
    ]
