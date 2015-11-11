# -*- coding: utf-8 -*-
from django.apps import apps
from django.test import Client, TestCase
from django.core.exceptions import ImproperlyConfigured


class TestReady(TestCase):

    def setUp(self):
        self.client = Client()
        self.app_config = apps.get_app_config('shorturl')

    def test_installed_apps(self):
        with self.assertRaises(ImproperlyConfigured):
            with self.modify_settings(INSTALLED_APPS={
                'remove': [
                    'django.contrib.staticfiles',
                ]
            }):
                self.app_config.ready()

    def test_middleware_classes(self):
        with self.assertRaises(ImproperlyConfigured):
            with self.modify_settings(MIDDLEWARE_CLASSES={
                'remove': [
                    'django.contrib.auth.middleware.AuthenticationMiddleware',
                ]
            }):
                self.app_config.ready()

    def test_middleware_classes_existence(self):
        with self.assertRaises(ImproperlyConfigured):
            with self.settings(MIDDLEWARE_CLASSES=None):
                self.app_config.ready()

