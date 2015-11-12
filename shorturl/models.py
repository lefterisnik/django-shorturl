# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .fields import BigAutoField
from .utils import *

shorturl_max_length = getattr(settings, 'SHORTURL_MAX_LENGTH', 23)

class ShortURL(models.Model):
    id = BigAutoField(primary_key=True)
    hash_id = models.BigIntegerField(unique=True, blank=True, null=True)
    user = models.ForeignKey(User)
    orig_url = models.URLField(_('original url'), max_length=200)
    c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'shorturl'

    def __unicode__(self):
        return '%s, %s, %s' % (self.orig_url, self.id, self.hash_id)

    @property
    def get_info(self):
        return self.shorturlinfo


class ShortURLInfo(models.Model):
    id = BigAutoField(primary_key=True)
    base_obj = models.OneToOneField(ShortURL)
    short_url = models.CharField(max_length=shorturl_max_length)
    views = models.BigIntegerField(default=0, editable=False)

    class Meta:
        app_label = 'shorturl'

    def __unicode__(self):
        return self.short_url
