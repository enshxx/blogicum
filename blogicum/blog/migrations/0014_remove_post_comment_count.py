# Generated by Django 3.2.16 on 2023-11-24 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_post_comment_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comment_count',
        ),
    ]
