from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NutrientSerializer
from recipes.models import Nutrient, ForeignAPI
from recipes.forms import InsertIngredients
import requests


spoonacular = ForeignAPI.objects.get(name='Spoonacular')
api_key = spoonacular.API_key
url = spoonacular.url


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Random Recipes': 'recipes-random',
        'List of Nutrients': 'nutrients-list',
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
    r = requests.get(f'{url}/random?apiKey={api_key}&tags=lunch&number=2').json()
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
    form = InsertIngredients()
    context = {'items': items, 'form': form}
    return Response(items)


