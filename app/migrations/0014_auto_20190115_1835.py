# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-15 18:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20190115_1830'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favourite',
            old_name='instrument',
            new_name='instruments',
        ),
    ]
