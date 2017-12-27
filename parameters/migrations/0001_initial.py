# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-26 20:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Название')),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Величина')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновленно')),
            ],
            options={
                'verbose_name': 'Атрибут',
                'verbose_name_plural': 'Атрибуты',
            },
        ),
        migrations.CreateModel(
            name='CategoryAtribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Название')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно?')),
            ],
            options={
                'verbose_name': 'Категория атрибута',
                'verbose_name_plural': 'Категории атрибутов',
            },
        ),
        migrations.CreateModel(
            name='CategoryParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Название')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно?')),
            ],
            options={
                'verbose_name': 'Категория параметра',
                'verbose_name_plural': 'Категории параметров',
            },
        ),
        migrations.CreateModel(
            name='ItemCategoryParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nmb', models.IntegerField(default=1, help_text='Укажите колличество изделий выбранной категории которые должны автоматически добавляться', verbose_name='Колличество')),
                ('item_paramater_do_more', models.BooleanField(default=False, help_text='Отметьте галочкой, если необходимо подбирать изделие на ступень выше', verbose_name='На ступень выше?')),
                ('item_paramater_revers', models.BooleanField(default=False, help_text='Отметьте галочкой, если необходимо увеличивать при реверсе', verbose_name='Увеличивать при Реверсе?')),
                ('item_paramater_bypass', models.BooleanField(default=False, help_text='Отметьте галочкой, если необходимо увеличивать при реверсе', verbose_name='Увеличивать при Bypass?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновленно')),
                ('item_category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='items.ItemCategory', verbose_name='Категория изделия')),
            ],
            options={
                'verbose_name': 'Категория изделия в параметре',
                'verbose_name_plural': 'Категории изделий в параметрах',
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Название')),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Величина')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновленно')),
                ('category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='parameters.CategoryParameter', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Параметр',
                'verbose_name_plural': 'Параметры',
            },
        ),
        migrations.AddField(
            model_name='itemcategoryparameter',
            name='parameter',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='parameters.Parameter', verbose_name='Тип пуска'),
        ),
        migrations.AddField(
            model_name='atribute',
            name='category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='parameters.CategoryAtribute', verbose_name='Категория'),
        ),
    ]
