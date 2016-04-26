# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MapObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('active', models.BooleanField()),
                ('location_long', models.DecimalField(decimal_places=6, max_digits=9)),
                ('location_lat', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
    ]