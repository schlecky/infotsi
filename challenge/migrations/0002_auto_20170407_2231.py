# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-07 20:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='epreuve',
            old_name='idEpreuve',
            new_name='numero',
        ),
        migrations.RemoveField(
            model_name='etudiant',
            name='idEtud',
        ),
    ]
