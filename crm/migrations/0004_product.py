# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-06 13:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20160905_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('price', models.IntegerField(default=0)),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Deal')),
            ],
        ),
    ]
