# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-21 00:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachersupport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='teachersupport.Course')),
            ],
            options={
                'verbose_name': 'Table',
                'verbose_name_plural': 'Tables',
            },
        ),
        migrations.RemoveField(
            model_name='day',
            name='Course',
        ),
        migrations.RemoveField(
            model_name='day',
            name='slots',
        ),
        migrations.AddField(
            model_name='table',
            name='Day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='day', to='teachersupport.Day'),
        ),
        migrations.AddField(
            model_name='table',
            name='Slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slot', to='teachersupport.Course'),
        ),
    ]
