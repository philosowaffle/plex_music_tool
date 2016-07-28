# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-28 01:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartPlaylists', '0004_querycondition_operator_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='lastfm_api_key',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='settings',
            name='lastfm_username',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='settings',
            name='plex_db_path',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
