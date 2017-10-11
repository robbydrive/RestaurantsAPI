# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-09 16:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20171009_0103'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'permissions': (('view_categories', 'Can view current menu (categories)'), ('create_categories', 'Can create new categories'), ('edit_categories', 'Can edit created categories'))},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': (('create_orders', 'Can create new orders'), ('view_orders', 'Can view orders'), ('edit_orders', 'Can edit created orders'))},
        ),
    ]