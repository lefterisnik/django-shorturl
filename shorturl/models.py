# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .fields import BigAutoField
from .utils import *


class ShortURL(models.Model):
    id = BigAutoField(primary_key=True)
    hash_id = models.BigIntegerField(unique=True, blank=True, null=True)
    user = models.ForeignKey(User)
    orig_url = models.URLField(_('original url'), max_length=200)
    c_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s, %s, %s' % (self.orig_url, self.id, self.hash_id)

    def save(self, *args, **kwargs):
        super(ShortURL, self).save(*args, **kwargs)
        msg = _('Short URL service reaches 23 maximum characters shorting')
        if self.hash_id:
            if len(dehydrate(self.hash_id)) > 23:
                self.delete()
                raise ValidationError(msg)
        elif self.id:
            if len(dehydrate(self.id)) > 23:
                self.delete()
                raise ValidationError(msg)


    @property
    def get_info(self):
        return self.shorturlinfo


class ShortURLInfo(models.Model):
    id = BigAutoField(primary_key=True)
    base_obj = models.OneToOneField(ShortURL)
    short_url = models.CharField(max_length=23)
    views = models.BigIntegerField(default=0, editable=False)

    def __unicode__(self):
        return self.short_url
