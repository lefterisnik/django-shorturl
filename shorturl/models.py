# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .fields import BigAutoField


class ShortURL(models.Model):
    id = BigAutoField(primary_key=True)
    user = models.ForeignKey(User)
    orig_url = models.URLField(_('original url'), max_length=200)
    c_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.orig_url


class ShortURLInfo(models.Model):
    base_obj = models.OneToOneField(ShortURL)
    short_url = models.CharField(max_length=28)
    views = models.BigIntegerField(default=0, editable=False)

    def __unicode__(self):
        return self.short_url

