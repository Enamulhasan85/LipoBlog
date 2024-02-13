# Generated by Django 5.0.2 on 2024-02-12 17:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0015_post_interactions_viewed'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='post_interactions',
            new_name='post_interaction',
        ),
        migrations.CreateModel(
            name='post_comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('post_interaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.post_interaction')),
            ],
        ),
    ]