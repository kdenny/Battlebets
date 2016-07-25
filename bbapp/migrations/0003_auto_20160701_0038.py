# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0002_auto_20160629_0402'),
    ]

    operations = [
        migrations.CreateModel(
            name='BetProposal',
            fields=[
                ('notification_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='bbapp.Notification')),
                ('sentat', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'date changed')),
                ('bet', models.ForeignKey(to='bbapp.Bet')),
            ],
            options={
            },
            bases=('bbapp.notification',),
        ),
        migrations.CreateModel(
            name='GameEnd',
            fields=[
                ('notification_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='bbapp.Notification')),
                ('winner', models.BooleanField(default=False)),
                ('endtime', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'date changed')),
                ('bet', models.ForeignKey(to='bbapp.Bet')),
            ],
            options={
            },
            bases=('bbapp.notification',),
        ),
        migrations.RemoveField(
            model_name='notification',
            name='bet',
        ),
    ]
