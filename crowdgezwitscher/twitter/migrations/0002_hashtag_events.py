# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-03 18:15
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20160919_1550'),
        ('twitter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hashtag',
            name='events',
            field=models.ManyToManyField(blank=True, related_name='hashtags', to='events.Event'),
        ),
    ]
