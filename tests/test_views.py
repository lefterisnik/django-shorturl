# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.core.urlresolvers import reverse


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