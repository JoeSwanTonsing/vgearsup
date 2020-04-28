# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-21 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20190221_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='contact',
        ),
        migrations.AddField(
            model_name='appuser',
            name='contact',
            field=models.ManyToManyField(null=True, related_name='_appuser_contact_+', to='app.AppUser'),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='photo',
            field=models.ImageField(default='instruments/instruments.jpg', upload_to='instruments/'),
        ),
    ]
