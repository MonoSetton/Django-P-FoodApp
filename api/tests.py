from django.test import TestCase, Client
from django.urls import reverse, resolve
from .views import api_overview, nutrients_list, recipes_random, recipes_ingredients, recipes_requirements
from recipes.models import Nutrient
import json
from unittest.mock import patch, Mock


class UrlsTestCase(TestCase):
    def test_api_overview(self):
        url = reverse('api')
        self.assertEqual(resolve(url).func, api_overview)

    def test_nutrients_list(self):
        url = reverse('nutrients-list')
        self.assertEqual(resolve(url).func, nutrients_list)

    def test_random_recipes(self):
        url = reverse('recipes-random')
        self.assertEqual(resolve(url).func, recipes_random)

    def test_recipes_ingredients(self):
        url = reverse('recipes-ingredients')
        self.assertEqual(resolve(url).func, recipes_ingredients)

    def test_recipes_requirements(self):
        url = reverse('recipes-requirements')
        self.assertEqual(resolve(url).func, recipes_requirements)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.api_urls_url = reverse('api')
        self.nutrients_list_url = reverse('nutrients-list')
        self.recipes_random_url = reverse('recipes-random')
        self.recipes_ingredients_url = reverse('recipes-ingredients')
        self.recipes_requirements_url = reverse('recipes-requirements')

    def test_api_overview(self):
        resp = self.client.get(self.api_urls_url)
        self.assertEqual(resp.status_code, 200)

    def test_nutrient_list_GET(self):
        resp = self.client.get(self.nutrients_list_url)
        self.assertEqual(resp.status_code, 200)

    def test_recipes_random_GET_image_found(self):
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                'recipes': [{'title': 'Recipe 1', 'id': 1, 'image': 'image1.jpg', 'readyInMinutes': 30, 'servings': 4}]}
            mock_get.return_value = mock_response

            resp = self.client.get(self.recipes_random_url)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Recipe 1', resp.content)
            self.assertIn(b'image1.jpg', resp.content)

    def test_recipes_random_GET_image_not_found(self):
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                'recipes': [{'title': 'Recipe 2', 'id': 2, 'readyInMinutes': 40, 'servings': 6}]}
            mock_get.return_value = mock_response

            resp = self.client.get(self.recipes_random_url)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Recipe 2', resp.content)
            self.assertIn(b'image_not_found', resp.content)

    def test_recipes_ingredients_POST(self):
        resp = self.client.post(self.recipes_ingredients_url)
        self.assertEqual(resp.status_code, 200)

    def test_recipes_ingredients_POST_image_found(self):
        dummy_data = {'ingredients': 'onion'}

        data_json = json.dumps(dummy_data)

        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [{'title': 'Recipe with Onion', 'id': 1, 'image': 'onion.jpg'}]
            mock_get.return_value = mock_response

            resp = self.client.post(self.recipes_ingredients_url, data=data_json, content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Recipe with Onion', resp.content)
            self.assertIn(b'onion.jpg', resp.content)

    def test_recipes_ingredients_image_not_found(self):
        dummy_data = {'ingredients': 'onion'}

        data_json = json.dumps(dummy_data)

        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [{'title': 'Recipe with Onion', 'id': 2}]
            mock_get.return_value = mock_response

            resp = self.client.post(self.recipes_ingredients_url, data=data_json, content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Recipe with Onion', resp.content)
            self.assertIn(b'image_not_found', resp.content)

    def test_recipes_requirements_POST(self):
        dummy_data = {'requirements': [['minCarbs', '5'], ['maxCarbs', '50']]}
        data_json = json.dumps(dummy_data)

        resp = self.client.post(self.recipes_requirements_url, data=data_json, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_recipes_requirements_POST_image_found(self):
        dummy_data = {'requirements': [['minCarbs', '5'], ['maxCarbs', '50']]}
        data_json = json.dumps(dummy_data)

        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [{'title': 'Recipe with Potato', 'id': 1, 'image': 'potato.jpg'}]
            mock_get.return_value = mock_response

            resp = self.client.post(self.recipes_requirements_url, data=data_json, content_type='application/json')

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Recipe with Potato', resp.content)
            self.assertIn(b'potato.jpg', resp.content)

    def test_recipes_requirements_POST_image_not_found(self):
        dummy_data = {'requirements': [['minCarbs', '5'], ['maxCarbs', '50']]}
        data_json = json.dumps(dummy_data)

        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [{'title': 'Recipe with Potato', 'id': 2}]
            mock_get.return_value = mock_response

            resp = self.client.post(self.recipes_requirements_url, data=data_json, content_type='application/json')

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Recipe with Potato', resp.content)
            self.assertIn(b'image_not_found', resp.content)

    def test_recipes_requirements_exception(self):
        dummy_data = {'requirements': [['minCarbs', '5'], ['maxCarbs', '50']]}
        data_json = json.dumps(dummy_data)

        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception('Failed to fetch data')

            resp = self.client.post(self.recipes_requirements_url, data=data_json, content_type='application/json')
            self.assertEqual(resp.status_code, 500)





