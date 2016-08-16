# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-24 13:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookLikeStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('like_count', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FacebookPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='unbenannt', max_length=100)),
                ('active', models.BooleanField(default=False)),
                ('location', models.CharField(max_length=100)),
                ('location_lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('location_long', models.DecimalField(decimal_places=6, max_digits=9)),
                ('notes', models.TextField(blank=True)),
                ('facebook_id', models.CharField(max_length=50)),
                ('events', models.ManyToManyField(blank=True, to='events.Event')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='facebooklikestatistic',
            name='page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='facebook.FacebookPage'),
        ),
    ]