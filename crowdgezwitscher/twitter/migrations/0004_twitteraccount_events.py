# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-03 20:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_remove_event_twitter_hashtags'),
        ('twitter', '0003_auto_20170103_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteraccount',
            name='events',
            field=models.ManyToManyField(blank=True, related_name='twitter_accounts', to='events.Event'),
        ),
    ]