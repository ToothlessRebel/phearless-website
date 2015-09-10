# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lootTracker', '0004_auto_20150909_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fleet',
            name='parent_fleet',
            field=models.ForeignKey(null=True, to='lootTracker.Fleet', blank=True),
        ),
    ]
