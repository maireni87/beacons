# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 03:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_profile_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, default='My location', max_length=1200),
        ),
    ]
