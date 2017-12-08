# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-06 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_communicationmethodsmodule'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulepicture',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='modulepicture',
            name='title',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Image title'),
        ),
        migrations.AlterField(
            model_name='modulepicture',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Image description'),
        ),
    ]