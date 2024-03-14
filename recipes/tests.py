from django.test import TestCase, RequestFactory, Client
from dotenv import load_dotenv
from django.conf import settings
from .models import CustomRecipe, Ingredient, Step, Nutrient
from .views import home, detail_recipes, requirements_recipes, custom_recipes, detail_custom_recipe, delete_custom_recipe, update_custom_recipe
from django.contrib.auth.models import User
from .forms import RecipeForm, IngredientFormSet, StepFormSet
from django.urls import reverse, resolve
from unittest.mock import MagicMock, patch
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


class UrlsTestCase(TestCase):
    def test_home_url(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    def test_detail_recipe_url(self):
        url = reverse('detail_recipes', args=['1'])
        self.assertEqual(resolve(url).func, detail_recipes)

    def test_insert_requirements_url(self):
        url = reverse('insert_requirements')
        self.assertEqual(resolve(url).func, requirements_recipes)

    def test_custom_recipes_url(self):
        url = reverse('custom_recipes')
        self.assertEqual(resolve(url).func, custom_recipes)

    def test_detail_custom_recipe_url(self):
        url = reverse('detail_custom_recipe', args=['1'])
        self.assertEqual(resolve(url).func, detail_custom_recipe)

    def test_delete_custom_recipe_url(self):
        url = reverse('delete_custom_recipe', args=['1'])
        self.assertEqual(resolve(url).func, delete_custom_recipe)

    def test_update_custom_recipe_url(self):
        url = reverse('update_custom_recipe', args=['1'])
        self.assertEqual(resolve(url).func, update_custom_recipe)


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


class RecipeViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.mock_response = MagicMock()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.custom_recipe = CustomRecipe.objects.create(name='Test Custom Recipe', image='testcustomrecipeimage.png',
                                                         author=self.user)
        self.ingredient = Ingredient.objects.create(name='Test Ingredient', recipe=self.custom_recipe)
        self.step = Step.objects.create(body='Test Step', recipe=self.custom_recipe)
        self.nutrient = Nutrient.objects.create(name='Test nutrient')

    @patch('recipes.views.requests.get')
    def test_home_view(self, mock_get):
        self.mock_response.json.return_value = {
            'recipes': [
                {'title': 'Recipe 1', 'id': 1, 'readyInMinutes': 30, 'servings': 4},
                {'title': 'Recipe 2', 'id': 2, 'readyInMinutes': 25, 'servings': 3, 'image': 'testimage1.png'}
            ]
        }
        mock_get.return_value = self.mock_response

        request = self.factory.get('home/')
        request.user = self.user
        response = home(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recipe 1')
        self.assertContains(response, 'Recipe 2')
        self.assertContains(response, 'image_not_found')

    @patch('recipes.views.requests.get')
    def test_detail_recipes(self, mock_get):
        self.mock_response.json.return_value = {'title': 'Recipe 1', 'id': 1, 'readyInMinutes': 30, 'servings': 4,
                 'sourceUrl': 'http://test.url'}
        mock_get.return_value = self.mock_response

        request = self.factory.get('/detail/1')
        request.user = self.user
        response = detail_recipes(request, pk=1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://test.url')

    def test_requirements_recipes(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('insert_requirements'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.nutrient)

    def test_detail_custom_recipe(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('detail_custom_recipe', args=[self.custom_recipe.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.custom_recipe)
        self.assertContains(response, self.ingredient)
        self.assertContains(response, self.step)

    def test_custom_recipes_POST_valid_data(self):
        self.client.login(username='testuser', password='12345')
        recipe_form_data = {
            'name': 'Test Recipe',
            'image': '',
        }

        ingredient_form_data = {
            'ingredient-TOTAL_FORMS': 6,
            'ingredient-INITIAL_FORMS': 0,
            'ingredient-MIN_NUM_FORMS': 1,
            'ingredient-MAX_NUM_FORMS': 1000,
            'ingredient-0-id': '',
            'ingredient-0-recipe': '',
            'ingredient-0-name': 'Ingredient 1',
        }

        step_form_data = {
            'step-TOTAL_FORMS': 8,
            'step-INITIAL_FORMS': 0,
            'step-MIN_NUM_FORMS': 1,
            'step-MAX_NUM_FORMS': 1000,
            'step-0-id': '',
            'step-0-recipe': '',
            'step-0-body': 'Step 1',
        }

        response = self.client.post(reverse('custom_recipes'), data={
            **recipe_form_data,
            **ingredient_form_data,
            **step_form_data
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(CustomRecipe.objects.filter(name='Test Recipe').exists())
        self.assertTrue(Ingredient.objects.filter(name='Ingredient 1').exists())
        self.assertTrue(Step.objects.filter(body='Step 1').exists())

    def test_update_custom_recipe_POST_not_author(self):
        self.client.login(username='testuser2', password='12345')
        response = self.client.post(reverse('update_custom_recipe', args=[self.custom_recipe.id]), follow=True)

        self.assertRedirects(response, '/profile/')

    def test_update_custom_recipe_POST_valid_author(self):
        self.client.login(username='testuser', password='12345')
        recipe_form_data = {
            'name': 'Test Recipe Updated',
            'image': '',
        }

        ingredient_form_data = {
            'ingredient-TOTAL_FORMS': 6,
            'ingredient-INITIAL_FORMS': 0,
            'ingredient-MIN_NUM_FORMS': 1,
            'ingredient-MAX_NUM_FORMS': 1000,
            'ingredient-0-id': '',
            'ingredient-0-recipe': '',
            'ingredient-0-name': 'Ingredient Updated',
        }

        step_form_data = {
            'step-TOTAL_FORMS': 8,
            'step-INITIAL_FORMS': 0,
            'step-MIN_NUM_FORMS': 1,
            'step-MAX_NUM_FORMS': 1000,
            'step-0-id': '',
            'step-0-recipe': '',
            'step-0-body': 'Step Updated',
        }

        response = self.client.post(reverse('update_custom_recipe', args=[self.custom_recipe.id]),
                                    data={**recipe_form_data,
                                          **ingredient_form_data,
                                          **step_form_data
                                          }, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(CustomRecipe.objects.filter(name='Test Recipe').exists())
        self.assertFalse(Ingredient.objects.filter(name='Ingredient 1').exists())
        self.assertFalse(Step.objects.filter(body='Step 1').exists())

        self.assertTrue(CustomRecipe.objects.filter(name='Test Recipe Updated').exists())
        self.assertTrue(Ingredient.objects.filter(name='Ingredient Updated').exists())
        self.assertTrue(Step.objects.filter(body='Step Updated').exists())

    def test_update_custom_recipe_GET_valid_author(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('update_custom_recipe', args=[self.custom_recipe.id]), follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertIn('recipe', response.context)
        self.assertIn('recipe_form', response.context)
        self.assertIn('ingredient_formset', response.context)



    def test_custom_recipes_GET(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('custom_recipes'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/create_custom_recipe.html')

        self.assertIn('recipe_form', response.context)
        self.assertIn('ingredient_formset', response.context)
        self.assertIn('step_formset', response.context)

    def test_delete_custom_recipe_GET(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('delete_custom_recipe', args=[self.custom_recipe.id]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/delete_custom_recipe.html')

    def test_delete_custom_recipe_POST(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('delete_custom_recipe', args=[self.custom_recipe.id]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/profile/')
        self.assertFalse(CustomRecipe.objects.filter(name='Test Custom Recipe').exists())

    def test_delete_custom_recipe_POST_not_an_author(self):
        self.client.login(username='testuser2', password='12345')
        response = self.client.get(reverse('delete_custom_recipe', args=[self.custom_recipe.id]), follow=True)

        self.assertEqual(response.status_code, 400)







