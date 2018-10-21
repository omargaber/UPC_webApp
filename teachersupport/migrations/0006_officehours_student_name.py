# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-10-21 06:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('teachersupport', '0005_remove_officehours_prof_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='officehours',
            name='student_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]