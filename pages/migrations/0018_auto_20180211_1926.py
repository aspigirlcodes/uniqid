# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-11 18:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0017_auto_20180130_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='is_visible',
            field=models.BooleanField(default=False, verbose_name='Is visible'),
        ),
    ]
