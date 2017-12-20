# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-08 13:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_auto_20171207_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(verbose_name='Position')),
                ('title', models.CharField(blank=True, default='', help_text='Choose a descriptive title for the contact. A good title may include the role of this contact, or the situation in which they can be contacted.', max_length=255, verbose_name='Contact title')),
                ('name', models.CharField(blank=True, default='', max_length=255, verbose_name='Name')),
                ('address', models.TextField(blank=True, default='', verbose_name='Address')),
                ('phone', models.CharField(blank=True, default='', max_length=255, verbose_name='Phone number')),
                ('email', models.EmailField(blank=True, default='', max_length=254, verbose_name='Email address')),
                ('extra', models.TextField(blank=True, default='', verbose_name='Extra comment')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.Page', verbose_name='Page')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
