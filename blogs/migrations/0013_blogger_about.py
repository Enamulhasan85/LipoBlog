# Generated by Django 4.2.5 on 2024-02-06 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0012_alter_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogger',
            name='about',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]