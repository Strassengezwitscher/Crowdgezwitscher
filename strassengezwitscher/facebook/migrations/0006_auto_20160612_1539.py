# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-12 15:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0005_auto_20160610_0349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facebookpage',
            name='url',
        ),
        migrations.AddField(
            model_name='facebookpage',
            name='facebook_id',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='facebookpage',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]