# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 03:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20151222_1935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='job',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
    ]