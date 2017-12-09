# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 19:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManufacturerCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Производитель изделия',
                'verbose_name_plural': 'Производители изделий',
            },
        ),
        migrations.RemoveField(
            model_name='itemimage',
            name='product',
        ),
        migrations.AddField(
            model_name='item',
            name='analog_input',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=4, verbose_name='Аналоговые входы [шт]'),
        ),
        migrations.AddField(
            model_name='item',
            name='analog_output',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=4, verbose_name='Аналоговые выходы [шт]'),
        ),
        migrations.AddField(
            model_name='item',
            name='currency',
            field=models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Валюта'),
        ),
        migrations.AddField(
            model_name='item',
            name='depth',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Глубина'),
        ),
        migrations.AddField(
            model_name='item',
            name='discret_input',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=4, verbose_name='Дискретные входы [шт]'),
        ),
        migrations.AddField(
            model_name='item',
            name='discret_output',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=4, verbose_name='Дискретные выходы [шт]'),
        ),
        migrations.AddField(
            model_name='item',
            name='ethernet',
            field=models.BooleanField(default=False, verbose_name='EtherNET'),
        ),
        migrations.AddField(
            model_name='item',
            name='force_input',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=2, verbose_name='Силовые входы [шт]'),
        ),
        migrations.AddField(
            model_name='item',
            name='height',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Высота'),
        ),
        migrations.AddField(
            model_name='item',
            name='power',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Мощность [кВт]'),
        ),
        migrations.AddField(
            model_name='item',
            name='profibus',
            field=models.BooleanField(default=False, verbose_name='ProfiBus'),
        ),
        migrations.AddField(
            model_name='item',
            name='profinet',
            field=models.BooleanField(default=False, verbose_name='ProfiNET'),
        ),
        migrations.AddField(
            model_name='item',
            name='rs484',
            field=models.BooleanField(default=False, verbose_name='RS484'),
        ),
        migrations.AddField(
            model_name='item',
            name='series',
            field=models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Серия'),
        ),
        migrations.AddField(
            model_name='item',
            name='temperature_input',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=4, verbose_name='Температурные входы [шт]'),
        ),
        migrations.AddField(
            model_name='item',
            name='voltage',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=7, verbose_name='Напряжение [В]'),
        ),
        migrations.AddField(
            model_name='item',
            name='width',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Ширина'),
        ),
        migrations.AddField(
            model_name='itemimage',
            name='item',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='items.Item', verbose_name='Изделие'),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='items.ItemCategory', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='item',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='item',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активно?'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='item',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновленно'),
        ),
        migrations.AlterField(
            model_name='itemimage',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='itemimage',
            name='image',
            field=models.ImageField(upload_to='items_images/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='itemimage',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активно?'),
        ),
        migrations.AlterField(
            model_name='itemimage',
            name='is_main',
            field=models.BooleanField(default=False, verbose_name='Основное?'),
        ),
        migrations.AlterField(
            model_name='itemimage',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновленно'),
        ),
        migrations.AddField(
            model_name='item',
            name='manufacturer',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='items.ManufacturerCategory', verbose_name='Производитель'),
        ),
    ]