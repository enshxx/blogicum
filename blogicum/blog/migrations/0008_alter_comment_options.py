# Generated by Django 3.2.16 on 2023-11-24 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created_at',)},
        ),
    ]