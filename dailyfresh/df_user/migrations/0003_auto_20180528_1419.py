# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-28 06:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_auto_20180528_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='uaddress',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='upc',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='uphone',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='ureceiver',
            field=models.CharField(max_length=20, null=True),
        ),
    ]