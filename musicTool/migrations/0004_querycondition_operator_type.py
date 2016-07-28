# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-27 00:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musicTool', '0003_auto_20160726_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='querycondition',
            name='operator_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='musicTool.QueryOperator'),
            preserve_default=False,
        ),
    ]
