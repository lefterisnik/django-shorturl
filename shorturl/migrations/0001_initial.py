# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import shorturl.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortURL',
            fields=[
                ('id', shorturl.fields.BigAutoField(serialize=False, primary_key=True)),
                ('orig_url', models.URLField(verbose_name='original url')),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShortURLInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_url', models.CharField(max_length=28)),
                ('views', models.BigIntegerField(default=0, editable=False)),
                ('base_obj', models.OneToOneField(to='shorturl.ShortURL')),
            ],
        ),
    ]
