# Generated by Django 5.0.2 on 2024-02-12 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0014_post_interactions'),
    ]

    operations = [
        migrations.AddField(
            model_name='post_interactions',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
    ]
