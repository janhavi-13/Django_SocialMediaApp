# Generated by Django 3.2.10 on 2023-11-30 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_post_followers_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='followers_count',
        ),
    ]
