# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-09 20:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0009_auto_20170409_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etudiant',
            name='user',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
