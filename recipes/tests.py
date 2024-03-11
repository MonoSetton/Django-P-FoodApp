from django.test import TestCase
from dotenv import load_dotenv
from django.conf import settings
from django.urls import reverse, resolve
from .views import home
from .models import Nutrient
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
        self.assertIn('code', r, msg=f"Status: {r['code']}, Message: {r['message']}")




