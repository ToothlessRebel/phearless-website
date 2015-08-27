# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lootTracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alliance',
            name='eve_id',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='eve_id',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='corporation',
            name='eve_id',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='eve_id',
            field=models.BigIntegerField(unique=True),
        ),
    ]
