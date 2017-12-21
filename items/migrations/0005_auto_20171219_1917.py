# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 19:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_auto_20171216_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('required', models.BooleanField(default=False, help_text='Отметьте галочкой, если необходимо обязательно добавить изделие', verbose_name='Обязательное устройство')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активная связь?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновленно')),
            ],
            options={
                'verbose_name': 'Дополнительные изделия',
                'verbose_name_plural': 'Дополнительное изделие',
            },
        ),
        migrations.AlterField(
            model_name='item',
            name='atributes',
            field=models.ManyToManyField(blank=True, default=None, to='parameters.Atribute', verbose_name='Атрибуты изделия'),
        ),
        migrations.AddField(
            model_name='additem',
            name='adding_item',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='add_item', to='items.Item', verbose_name='Дополнительное изделие'),
        ),
        migrations.AddField(
            model_name='additem',
            name='main_item',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_item', to='items.Item', verbose_name='Основное изделие'),
        ),
        migrations.AlterUniqueTogether(
            name='additem',
            unique_together=set([('main_item', 'adding_item')]),
        ),
    ]