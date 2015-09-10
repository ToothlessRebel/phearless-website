# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lootTracker', '0003_fleet_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fleet',
            name='name',
            field=models.CharField(max_length=250, default=''),
        ),
    ]
