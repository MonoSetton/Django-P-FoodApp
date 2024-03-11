from django.test import TestCase
from dotenv import load_dotenv
from django.conf import settings
from .models import CustomRecipe, Ingredient, Step, Nutrient
from django.contrib.auth.models import User
import requests
import os
load_dotenv(os.path.join(settings.BASE_DIR, ".env"))


class APITestCase(TestCase):
    api_key = os.getenv("api_key")
    api_url = os.getenv("api_url")

    def test_api_key(self):
        self.assertIsNotNone(self.api_key, msg="Couldn't find an api key")

    def test_api_url(self):
        self.assertIsNotNone(self.api_url, msg="Couldn't find an api url")

    def test_api_call_status(self):
        r = requests.get(f'{self.api_url}/random?apiKey={self.api_key}&number=1').json()
        self.assertNotIn('code', r)


class RecipesModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.nutrient1 = Nutrient.objects.create(name='test')
        self.customrecipe1 = CustomRecipe.objects.create(name='test', image='test.png', author=self.user)
        self.ingredient1 = Ingredient.objects.create(name='test', recipe=self.customrecipe1)
        self.step1 = Step.objects.create(body='test', recipe=self.customrecipe1)

    def test_nutrient(self):
        self.assertEqual(str(self.nutrient1), 'test')

    def test_customer_recipe(self):
        self.assertEqual(str(self.customrecipe1), 'test')

    def test_ingredient(self):
        self.assertEqual(str(self.ingredient1), 'test')

    def test_step(self):
        self.assertEqual(str(self.step1), 'test')
