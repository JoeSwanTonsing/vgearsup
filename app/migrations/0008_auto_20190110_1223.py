# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-10 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20190108_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='auction',
            field=models.BooleanField(default=False),
        ),
    ]
