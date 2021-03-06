# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-14 15:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20170514_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='qualification',
            name='languages',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='jobs.Language'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='language',
            name='proficiency',
            field=models.CharField(choices=[('1_basic', '1_basic'), ('2_intermediate', '2_intermediate'), ('3_business', '3_business'), ('4_fluent', '4_fluent'), ('5_native', '5_native')], max_length=50),
        ),
        migrations.AlterField(
            model_name='skill',
            name='proficiency',
            field=models.CharField(choices=[('1_beginner', '1_beginner'), ('2_advanced', '2_advanced'), ('3_expert', '3_expert')], max_length=50),
        ),
    ]
