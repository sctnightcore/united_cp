# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-30 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unitedcp', '0002_auto_20170628_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='item_description',
            field=models.TextField(blank=True, default='Item description', max_length=5000, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='item_discount_from',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Discount date starts'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='item_discount_until',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Discount date ends'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='item_sale_ends',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Sale date end'),
        ),
    ]