# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(related_name='notifications', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
