# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0004_auto_20171216_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcategoryparameter',
            name='item_paramater_do_more',
            field=models.BooleanField(default=True, help_text='Отметьте галочкой, если необходимо подбирать изделие на ступень выше', verbose_name='На ступень выше?'),
        ),
        migrations.AlterField(
            model_name='itemcategoryparameter',
            name='nmb',
            field=models.IntegerField(default=1, help_text='Укажите колличество изделий выбранной категории которые должны автоматически добавляться', verbose_name='Колличество'),
        ),
    ]