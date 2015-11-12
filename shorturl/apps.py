# -*- coding: utf-8 -*-
from django.conf import settings
from django.apps import AppConfig
from django.db.models.signals import post_save
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from .signals import *


class ShortURLConfig(AppConfig):
    name = 'shorturl'
    verbose_name = _('Short URL')

    def ready(self):
        """
        Test settings
        """
        # Exam template backend
        try:
            django_backend = [x for x in settings.TEMPLATES
                              if x['BACKEND'] == 'django.template.backends.django.DjangoTemplates'][0]
        except IndexError:
            raise ImproperlyConfigured("Short URL requires 'django.template.backends.django.DjangoTemplates' "
                                       "as backend at template settings.")

        # Exam context processors
        context_processors = django_backend.get('OPTIONS', {}).get('context_processors', [])
        if ('django.core.context_processors.request' not in context_processors and
                    'django.template.context_processors.request' not in context_processors):
            raise ImproperlyConfigured("Short URL requires 'django.template.context_processors.request' in "
                                       "'django.template.backends.django.DjangoTemplates' context processors.")

        # Exam MIDDLEWARE_CLASSES existence
        middleware_classes = getattr(settings, 'MIDDLEWARE_CLASSES', None)
        if middleware_classes is None:
            raise ImproperlyConfigured("Short URL requires 'MIDDLEWARE_CLASSES' in settings file.")

        if 'django.contrib.auth.middleware.AuthenticationMiddleware' not in middleware_classes:
            raise ImproperlyConfigured("Short URL requires 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                                       " in 'MIDDLEWARE_CLASSES'.")

        # Exam INSTALLED APPS
        if 'django.contrib.staticfiles' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Short URL requires 'django.contrib.staticfiles' in 'INSTALLED_APPS'.")

        # Set default max length at short url
        shorturl_max_length = getattr(settings, 'SHORTURL_MAX_LENGTH', None)
        if shorturl_max_length is None:
            setattr(settings, 'SHORTURL_MAX_LENGTH', 23)

        # Connect signals
        try:
            ShortURL = self.get_model('ShortURL')
            post_save.connect(update_info, ShortURL)
        except LookupError:
            raise ImproperlyConfigured("Short URL requires 'ShortURL' model.")