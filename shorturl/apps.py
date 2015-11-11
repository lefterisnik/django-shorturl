# -*- coding: utf-8 -*-
from django.conf import settings
from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _


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

        if 'django.contrib.staticfiles' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Short URL requires 'django.contrib.staticfiles' in 'INSTALLED_APPS'.")