# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-02 16:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('CHF', 'CHF'), ('EUR', 'EUR'), ('USD', 'USD'), ('CAD', 'CAD')], max_length=3, verbose_name='currency')),
                ('_unit_price', models.DecimalField(decimal_places=10, max_digits=18, verbose_name='unit price')),
                ('tax_included', models.BooleanField(default=True, help_text='Is tax included in given unit price?', verbose_name='tax included')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='cromio.Product', verbose_name='product')),
            ],
            options={
                'ordering': ['-id'],
                'get_latest_by': 'id',
                'verbose_name': 'price',
                'verbose_name_plural': 'prices',
            },
        ),
    ]
