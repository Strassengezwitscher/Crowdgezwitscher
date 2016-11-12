# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-11 23:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20160919_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(upload_to=events.models.Attachment.get_path_and_set_filename)),
                ('name', models.CharField(max_length=50)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='events.Event')),
            ],
        ),
    ]