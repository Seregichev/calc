# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-10 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_item_current'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='type_current',
            field=models.CharField(blank=True, default=None, max_length=3, null=True, verbose_name='Вид тока'),
        ),
    ]