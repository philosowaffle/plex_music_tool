# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-20 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicTool', '0007_async_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='gracenote_client_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='settings',
            name='gracenote_user_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
