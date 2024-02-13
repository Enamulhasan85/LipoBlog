# Generated by Django 5.0.2 on 2024-02-12 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0013_blogger_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='post_interactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('liked', models.BooleanField(default=False)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('blogger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.blogger')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.post')),
            ],
        ),
    ]