from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NutrientSerializer
from recipes.models import Nutrient, ForeignAPI
import requests


spoonacular = ForeignAPI.objects.get(name='Spoonacular')
api_key = spoonacular.API_key
url = spoonacular.url


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Random Recipes': 'recipes-random',
        'List of Nutrients': 'nutrients-list',
        'Recipes from Ingredients': 'recipes-ingredients',
        'Recipes from Requirements': 'recipes-requirements',
    }
    return Response(api_urls)


@api_view(['GET'])
def nutrients_list(request):
    nutrients = Nutrient.objects.all()
    serializer = NutrientSerializer(nutrients, many=True).data
    return Response(serializer)


@api_view(['GET'])
def recipes_random(request):
    titles, images, ids, readyInMinutes, servings = [], [], [], [], []
    r = requests.get(f'{url}/random?apiKey={api_key}&tags=lunch&number=6').json()
    r = r['recipes']
    for index, item in enumerate(r):
        titles.append(r[index]['title'])
        ids.append(r[index]['id'])
        readyInMinutes.append(r[index]['readyInMinutes'])
        servings.append(r[index]['servings'])
        if 'image' in r[index]:
            images.append(r[index]['image'])
        else:
            images.append('image_not_found')
    items = zip(titles, images, ids, readyInMinutes, servings)
    return Response(items)


@api_view(['POST'])
def recipes_ingredients(request):
    titles, images, ids = [], [], []
    conditionals = 'number=6&ranking=1&ignorePantry=false'
    ingredients = request.data.get('ingredients')
    r = requests.get(f'{url}/findByIngredients?apiKey={api_key}&'
                     f'{conditionals}&'
                     f'ingredients={ingredients}').json()
    for index, item in enumerate(r):
        titles.append(r[index]['title'])
        ids.append(r[index]['id'])
        if 'image' in r[index]:
            images.append(r[index]['image'])
        else:
            images.append('image_not_found')
    items = zip(titles, images, ids)
    return Response(items)


@api_view(['POST'])
def recipes_requirements(request):
    titles, images, ids = [], [], []
    query = ''
    for key, value in request.data.get('requirements'):
        if value != '':
            query += f'&{key}={value}'
    try:
        r = requests.get(f'{url}/findByNutrients?apiKey={api_key}&number=6&random=true{query}').json()
        for index, item in enumerate(r):
            titles.append(r[index]['title'])
            ids.append(r[index]['id'])
            if 'image' in r[index]:
                images.append(r[index]['image'])
            else:
                images.append('image_not_found')
        items = list(zip(titles, images, ids))
        return Response(items)
    except Exception as e:
        return Response({'error': 'Failed to fetch data'}, status=500)



