# Generated by Django 4.1.1 on 2022-12-10 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_alter_post_blogtext'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogger',
            name='education',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='blogger',
            name='occupation',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
