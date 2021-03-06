# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-11-29 23:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('billing', '0002_auto_20181129_0437'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(choices=[('fatura', 'Fatura'), ('kargo', 'Kargo')], max_length=120)),
                ('address_line_1', models.CharField(max_length=200)),
                ('address_line_2', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(default='Izmir', max_length=120)),
                ('country', models.CharField(default='Turkiye', max_length=120)),
                ('state', models.CharField(max_length=120)),
                ('billing_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.BiliingProfile')),
            ],
        ),
    ]
