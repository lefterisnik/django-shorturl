# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings


@override_settings(ROOT_URLCONF='tests.urls')
class TestAdminModel(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_superuser(username='admin', email='', password='admin')

    def test_get_model_access(self):
        self.client.login(username='admin', password='admin')

        response = self.client.get('/admin/shorturl/', follow=True)
        self.assertEqual(response.status_code, 200)