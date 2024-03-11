from django.test import TestCase, Client
from django.urls import reverse, resolve
from .views import profile
from recipes.models import CustomRecipe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from accounts.forms import RegisterForm
from accounts.views import sign_up


class UrlsTestCase(TestCase):
    def test_sign_up(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, sign_up)

    def test_profile(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, profile)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile_url = reverse('profile')
        self.sign_up_url = reverse('signup')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.custom_recipe1 = CustomRecipe.objects.create(author=self.user, name='Recipe 1', image='Image1.png')
        self.custom_recipe2 = CustomRecipe.objects.create(author=self.user, name='Recipe 2', image='Image2.png')

    def test_profile(self):
        login = self.client.login(username='testuser', password='password123')
        resp = self.client.get(self.profile_url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.custom_recipe1, resp.context['custom_recipes'][0])
        self.assertEqual(self.custom_recipe2, resp.context['custom_recipes'][1])

    def test_signup_POST(self):
        data = {
            'username': 'signuptestuser',
            'email': 'test@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        }
        resp = self.client.post(self.sign_up_url, data)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username='signuptestuser').exists())

        user = authenticate(username='signuptestuser', password='TestPassword123')
        self.assertTrue(user.is_authenticated)

    def test_signup_POST_invalid_form(self):
        data = {
            'username': '',
            'email': 'test@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        }
        resp = self.client.post(self.sign_up_url, data)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(User.objects.filter(username='').exists())

    def test_signup_GET(self):
        resp = self.client.get(self.sign_up_url)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.context['form'], RegisterForm)