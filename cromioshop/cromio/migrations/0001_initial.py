# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-08 14:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderWithData',
            fields=[
                ('order_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop.Order')),
            ],
            options={
                'abstract': False,
            },
            bases=('shop.order',),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('configurations', models.TextField(blank=True, verbose_name='configurations')),
                ('accessories', models.TextField(blank=True, verbose_name='accessories')),
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
                ('currency', models.CharField(choices=[(b'EUR', b'EUR')], max_length=3, verbose_name='currency')),
                ('_unit_price', models.DecimalField(decimal_places=10, max_digits=18, verbose_name='unit price')),
                ('tax_included', models.BooleanField(default=True, help_text='Is tax included in given unit price?', verbose_name='tax included')),
                ('material', models.CharField(blank=True, max_length=300, null=True)),
                ('size', models.CharField(blank=True, max_length=300, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='cromio.Product', verbose_name='product')),
                ('tax_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='shop.TaxClass', verbose_name='tax class')),
            ],
            options={
                'ordering': ['-id'],
                'get_latest_by': 'id',
                'verbose_name': 'price',
                'verbose_name_plural': 'prices',
            },
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('price', models.FloatField()),
            ],
        ),
    ]
