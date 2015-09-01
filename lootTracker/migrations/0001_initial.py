# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alliance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('eve_id', models.BigIntegerField(unique=True)),
                ('portrait', models.FileField(upload_to='eve/portraits/alliance')),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('eve_id', models.BigIntegerField(unique=True)),
                ('portrait', models.FileField(upload_to='eve/portraits/character')),
            ],
        ),
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('eve_id', models.BigIntegerField(unique=True)),
                ('portrait', models.FileField(upload_to='eve/portraits/corporation')),
                ('alliance', models.ForeignKey(to='lootTracker.Alliance')),
            ],
        ),
        migrations.CreateModel(
            name='Drop',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('item_current_value', models.DecimalField(decimal_places=2, max_digits=50)),
            ],
        ),
        migrations.CreateModel(
            name='Fleet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('finalized', models.BooleanField(default=False)),
                ('corporation', models.ForeignKey(to='lootTracker.Corporation')),
                ('members', models.ManyToManyField(to='lootTracker.Character')),
            ],
        ),
        migrations.CreateModel(
            name='FleetRestriction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='FleetType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('icon', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('eve_id', models.BigIntegerField(unique=True)),
                ('icon', models.FileField(upload_to='eve/portraits/items')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('value', models.BigIntegerField()),
                ('character', models.ForeignKey(to='lootTracker.Character')),
            ],
        ),
        migrations.CreateModel(
            name='Treasury',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200, default='')),
                ('value', models.BigIntegerField()),
                ('corporation', models.ForeignKey(to='lootTracker.Corporation')),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='treasury',
            field=models.ForeignKey(to='lootTracker.Treasury'),
        ),
        migrations.AddField(
            model_name='fleet',
            name='restriction',
            field=models.ForeignKey(null=True, to='lootTracker.FleetRestriction'),
        ),
        migrations.AddField(
            model_name='fleet',
            name='type',
            field=models.ForeignKey(null=True, to='lootTracker.FleetType'),
        ),
        migrations.AddField(
            model_name='drop',
            name='fleet',
            field=models.ForeignKey(to='lootTracker.Fleet'),
        ),
        migrations.AddField(
            model_name='drop',
            name='item',
            field=models.ForeignKey(to='lootTracker.Item'),
        ),
        migrations.AddField(
            model_name='character',
            name='corporation',
            field=models.ForeignKey(to='lootTracker.Corporation'),
        ),
        migrations.AddField(
            model_name='character',
            name='user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
