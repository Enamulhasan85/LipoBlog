# Generated by Django 4.1.1 on 2022-12-12 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_bloglayout_category_blogger_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloglayout',
            name='author',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, to='blogs.blogger'),
            preserve_default=False,
        ),
    ]