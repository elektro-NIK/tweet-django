# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48, unique=True)),
                ('tweet', models.ManyToManyField(to='tweets.Tweet')),
            ],
        ),
    ]
