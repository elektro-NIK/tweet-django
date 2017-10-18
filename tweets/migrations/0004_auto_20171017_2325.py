# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 20:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0003_comment_like_retweet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='tweet',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='like',
            name='tweet',
        ),
        migrations.RemoveField(
            model_name='like',
            name='users',
        ),
        migrations.RemoveField(
            model_name='retweet',
            name='tweet',
        ),
        migrations.RemoveField(
            model_name='retweet',
            name='users',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.DeleteModel(
            name='Retweet',
        ),
    ]