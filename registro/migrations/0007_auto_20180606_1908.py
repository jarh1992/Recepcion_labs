# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-07 00:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0006_auto_20180606_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registro.Program'),
        ),
    ]