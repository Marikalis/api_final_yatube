# Generated by Django 2.2.16 on 2021-12-12 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_follow_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='slug',
        ),
    ]