# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-24 23:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicTool', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='description',
            field=models.CharField(default='default description', max_length=500),
            preserve_default=False,
        ),
    ]