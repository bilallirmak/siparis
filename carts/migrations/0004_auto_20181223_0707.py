# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-23 04:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_auto_20181218_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
    ]