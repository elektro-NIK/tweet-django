# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0002_hashtag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='country',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
