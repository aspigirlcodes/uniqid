# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-13 16:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_sensorymodule'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', help_text='Choose a descriptive title for the contact. A good title may include the role of this contact, or the situation in which they can be contacted.', max_length=255, verbose_name='Contact title')),
                ('name', models.CharField(blank=True, default='', max_length=255, verbose_name='Name')),
                ('address', models.TextField(blank=True, default='', verbose_name='Address')),
                ('phone', models.CharField(blank=True, default='', max_length=255, verbose_name='Phone number')),
                ('email', models.EmailField(blank=True, default='', max_length=254, verbose_name='Email address')),
                ('extra', models.TextField(blank=True, default='', verbose_name='Extra comment')),
            ],
        ),
        migrations.RemoveField(
            model_name='contactmodule',
            name='address',
        ),
        migrations.RemoveField(
            model_name='contactmodule',
            name='email',
        ),
        migrations.RemoveField(
            model_name='contactmodule',
            name='extra',
        ),
        migrations.RemoveField(
            model_name='contactmodule',
            name='name',
        ),
        migrations.RemoveField(
            model_name='contactmodule',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='contactmodule',
            name='title',
        ),
        migrations.AddField(
            model_name='modulecontact',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.ContactModule', verbose_name='module'),
        ),
    ]
