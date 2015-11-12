# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from shorturl.models import *


class AnonymousViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_redirect_to_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_right_redirection(self):
        response = self.client.get('/', follow=True)
        login_url = reverse('login')
        self.assertIn(login_url, response.redirect_chain[0][0])


class AuthenticatedViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_superuser(username='admin', email='', password='admin')

    def test_get_home_access(self):
        self.client.login(username='admin', password='admin')

        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_urls_access(self):
        self.client.login(username='admin', password='admin')

        response = self.client.get('/retrieve-urls/')
        self.assertEqual(response.status_code, 200)

    def test_get_original_access(self):
        self.client.login(username='admin', password='admin')

        response = self.client.get('/retrieve-original/')
        self.assertEqual(response.status_code, 200)

    def test_post_home_post(self):
        self.client.login(username='admin', password='admin')

        response = self.client.post('/', {'url': 'http://www.example.com'})
        self.assertEqual(response.status_code, 200)

        obj = ShortURL.objects.get(orig_url='http://www.example.com')
        short_url = 'http://example.com/%s' % obj.get_info.short_url
        self.assertIn(short_url, response.content)

    def test_get_url_access_with_objs(self):
        self.client.login(username='admin', password='admin')
        obj = ShortURL.objects.create(user=self.user, orig_url='http://www.example.com')

        response = self.client.get('/retrieve-urls/')
        self.assertEqual(response.status_code, 200)

        self.assertIn(obj.orig_url, response.content)

    def test_get_detail_access(self):
        self.client.login(username='admin', password='admin')
        obj = ShortURL.objects.create(user=self.user, orig_url='http://www.example.com')

        response = self.client.get('/retrieve-details/%s/' % obj.id)
        self.assertEqual(response.status_code, 200)

    def test_redirect_service(self):
        self.client.login(username='admin', password='admin')
        obj = ShortURL.objects.create(user=self.user, orig_url='http://www.example.com')

        response = self.client.get('/%s/' % obj.get_info.short_url)
        self.assertEqual(response.status_code, 302)
