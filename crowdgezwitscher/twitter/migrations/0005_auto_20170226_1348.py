# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-26 13:48
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0004_twitteraccount_events'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitteraccount',
            name='last_known_tweet_id',
            field=models.CharField(default=0, max_length=20),
        ),
    ]
