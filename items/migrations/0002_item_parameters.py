# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-16 18:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0003_auto_20171216_1143'),
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='parameters',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='parameters.Parameter', verbose_name='Атрибуты изделия'),
        ),
    ]
