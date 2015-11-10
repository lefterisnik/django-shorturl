# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth.views import login, logout

from social.backends.google import GooglePlusAuth

from .views import *

context = dict(
    plus_id=getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
    plus_scope=' '.join(GooglePlusAuth.DEFAULT_SCOPE),
)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/', login, {'template_name': 'shorturl/login.html', 'extra_context': context}, name='login'),
    url(r'^logout/', logout, {'template_name': 'shorturl/logout.html'}, name='logout'),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social'))

]