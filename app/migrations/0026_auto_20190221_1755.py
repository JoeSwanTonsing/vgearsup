# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-21 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20190217_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='favourite',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='instrument',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]