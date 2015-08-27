# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('lootTracker', '0001_initial'), ('lootTracker', '0002_auto_20150827_0135')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alliance',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('eve_id', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('eve_id', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('eve_id', models.BigIntegerField()),
                ('alliance', models.ForeignKey(to='lootTracker.Alliance')),
            ],
        ),
        migrations.CreateModel(
            name='Drop',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('item_current_value', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Fleet',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('corporation', models.ForeignKey(to='lootTracker.Corporation')),
                ('members', models.ManyToManyField(to='lootTracker.Character')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('eve_id', models.BigIntegerField(unique=True)),
                ('value', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('value', models.BigIntegerField()),
                ('character', models.ForeignKey(to='lootTracker.Character')),
            ],
        ),
        migrations.CreateModel(
            name='Treasury',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
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
    ]
