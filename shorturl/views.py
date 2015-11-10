# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from social.backends.google import GooglePlusAuth


@login_required(login_url=reverse_lazy('login'))
def index(request):
    context = dict(
        plus_id=getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
        plus_scope=' '.join(GooglePlusAuth.DEFAULT_SCOPE),
    )
    return render(request, 'shorturl/index.html', context)