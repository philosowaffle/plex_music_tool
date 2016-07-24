# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-24 22:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('query', models.CharField(max_length=350)),
                ('last_updated', models.DateTimeField(verbose_name='last updated')),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plex_db_path', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('artist', models.CharField(max_length=50)),
                ('last_played', models.DateTimeField(verbose_name='last played')),
                ('play_count', models.IntegerField(default=0)),
                ('last_updated', models.DateTimeField(verbose_name='last upadated')),
            ],
        ),
    ]
