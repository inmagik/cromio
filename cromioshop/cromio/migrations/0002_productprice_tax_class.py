# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-02 16:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cromio', '0001_initial'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productprice',
            name='tax_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='shop.TaxClass', verbose_name='tax class'),
        ),
    ]
