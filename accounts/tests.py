from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve
from .views import sign_up, profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


class UrlsTestCase(TestCase):
    def test_sign_up(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, sign_up)

    def test_profile(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, profile)



