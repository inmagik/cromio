# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-05 09:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cromio', '0004_auto_20160905_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='accessories',
            field=models.TextField(blank=True, verbose_name='accessories'),
        ),
    ]
