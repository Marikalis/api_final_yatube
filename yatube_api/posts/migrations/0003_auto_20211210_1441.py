# Generated by Django 2.2.16 on 2021-12-10 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20211210_1437'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='Unique_name_follow',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'following'), name='Unique_name_follow'),
        ),
    ]