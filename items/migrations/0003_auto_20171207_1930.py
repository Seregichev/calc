# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 19:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_auto_20171207_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemManufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(blank=True, default=None, max_length=5, null=True)),
                ('name', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Производитель изделия',
                'verbose_name_plural': 'Производители изделий',
            },
        ),
        migrations.AlterField(
            model_name='item',
            name='manufacturer',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='items.ItemManufacturer', verbose_name='Производитель'),
        ),
        migrations.DeleteModel(
            name='ManufacturerCategory',
        ),
    ]