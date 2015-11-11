# -*- coding: utf-8 -*-
from django import template

from ..utils import *

register = template.Library()

@register.simple_tag(takes_context=True)
def full_shorturl(context, short_url):
    request = context['request']
    return create_full_shorturl(request, short_url)