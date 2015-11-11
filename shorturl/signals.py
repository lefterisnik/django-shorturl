# -*- coding: utf-8 -*-
from .utils import *
from .models import *


def update_info(sender, instance, created, **kwargs):
    if created:
        if instance.hash_id:
            short_url = dehydrate(instance.hash_id)
        else:
            short_url = dehydrate(instance.id)
        ShortURLInfo.objects.create(base_obj=instance, short_url=short_url)
