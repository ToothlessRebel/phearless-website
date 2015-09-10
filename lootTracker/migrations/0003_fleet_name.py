# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lootTracker', '0002_fleet_parent_fleet'),
    ]

    operations = [
        migrations.AddField(
            model_name='fleet',
            name='name',
            field=models.TextField(default=''),
        ),
    ]
