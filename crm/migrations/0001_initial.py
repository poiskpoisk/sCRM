# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-05 11:38
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('second_name', models.CharField(max_length=30)),
                ('avatar', models.ImageField(upload_to='/pic/')),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('company', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=50)),
                ('mobile_phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('email_address', models.EmailField(max_length=80)),
                ('brith_data', models.DateField()),
                ('comment', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Deals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_time', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('E', 'First contact'), ('D', 'Decision making'), ('H', 'Harmonization of contract'), ('S', 'The contract is signed'), ('P', 'Checkout paid'), ('E', 'Contract executed successfully'), ('A', 'DEAD DEAL')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='SalesPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('second_name', models.CharField(max_length=30)),
                ('avatar', models.ImageField(upload_to='/pic/')),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('email_address', models.EmailField(max_length=80)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Todos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('E', 'Email'), ('C', 'Phone call'), ('O', 'Other')], max_length=1)),
                ('action_description', models.TextField()),
                ('data_time', models.DateTimeField()),
                ('sales_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.SalesPerson')),
            ],
        ),
        migrations.AddField(
            model_name='deals',
            name='sales_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.SalesPerson'),
        ),
        migrations.AddField(
            model_name='contacts',
            name='sales_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.SalesPerson'),
        ),
    ]
