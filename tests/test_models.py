# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from shorturl.models import *


class TestShortURLModel(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_superuser(username='admin', email='', password='admin')
        self.obj = ShortURL.objects.create(user=self.user, orig_url='http://example.com')

    def test_unicode_return(self):
        self.assertEqual(unicode(self.obj), '%s, %s, %s' %(self.obj.orig_url, self.obj.id, self.obj.hash_id))


class TestShortURLInfoModel(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_superuser(username='admin', email='', password='admin')
        self.p_obj = ShortURL.objects.create(user=self.user, orig_url='http://example.com')
        #self.obj = ShortURLInfo(base_obj=self.p_obj, short_url=)

    def test_unicode_return(self):
        self.assertEqual(unicode(self.p_obj.get_info), self.p_obj.get_info.short_url)