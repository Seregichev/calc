# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-15 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0009_auto_20180115_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='area',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Площадь'),
        ),
    ]
