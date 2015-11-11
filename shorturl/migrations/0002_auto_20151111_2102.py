# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import shorturl.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shorturl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shorturl',
            name='hash_id',
            field=models.BigIntegerField(unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='shorturlinfo',
            name='id',
            field=shorturl.fields.BigAutoField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='shorturlinfo',
            name='short_url',
            field=models.CharField(max_length=23),
        ),
    ]
