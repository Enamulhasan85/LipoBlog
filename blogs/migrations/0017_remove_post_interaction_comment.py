# Generated by Django 5.0.2 on 2024-02-12 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0016_rename_post_interactions_post_interaction_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post_interaction',
            name='comment',
        ),
    ]