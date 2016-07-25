# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bet_selection', models.CharField(default=b'', max_length=20)),
                ('bet_status', models.CharField(default=b'', max_length=20)),
                ('bet_value', models.DecimalField(max_digits=6, decimal_places=2)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'date created')),
                ('changed_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'date changed')),
                ('bet_type', models.CharField(default=b'even', max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('gamekey', models.CharField(default=b'', max_length=200, unique=True, serialize=False, primary_key=True)),
                ('league', models.CharField(default=b'', max_length=5)),
                ('home_team', models.CharField(default=b'', max_length=200)),
                ('home_odds', models.CharField(default=b'', max_length=5)),
                ('home_short', models.CharField(default=b'', max_length=5)),
                ('away_team', models.CharField(default=b'', max_length=200)),
                ('away_odds', models.CharField(default=b'', max_length=5)),
                ('away_short', models.CharField(default=b'', max_length=5)),
                ('status', models.CharField(default=b'', max_length=20)),
                ('game_time', models.CharField(default=b'', max_length=20)),
                ('date', models.CharField(default=b'', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seen', models.BooleanField(default=False)),
                ('bet', models.ForeignKey(to='bbapp.Bet')),
                ('sender', models.ForeignKey(related_name='notification', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(default=b'', max_length=200, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bet',
            name='game',
            field=models.ForeignKey(to='bbapp.Game'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bet',
            name='user1',
            field=models.ForeignKey(related_name='user2', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bet',
            name='user2',
            field=models.ForeignKey(related_name='user1', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
