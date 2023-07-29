from django.shortcuts import render, redirect
from .forms import InsertIngredients
import requests


api_key = '99aa443bda864d698ad5ac6db226c843'
url = "https://api.spoonacular.com/recipes"


def home(request):
    titles = []
    images = []
    ids = []
    r = requests.get(f'{url}/random?apiKey={api_key}&tags=lunch&number=9').json()
    r = r['recipes']
    for index, item in enumerate(r):
        if 'image' in r[index]:
            titles.append(r[index]['title'])
            images.append(r[index]['image'])
            ids.append(r[index]['id'])
    items = zip(titles, images, ids)
    context = {'items': items}
    return render(request, 'recipes/home.html', context)


def detail_recipes(request, pk):
    r = requests.get(f'{url}/{pk}/information?apiKey={api_key}&includeNutrition=false').json()
    sourceURL = r['sourceUrl']
    return redirect(sourceURL)


def ingredients_recipes(request):
    if request.method == 'POST':
        titles, images, ids = [], [], []
        conditionals = 'number=6&ranking=1&ignorePantry=false'
        ingredients = request.POST.get('ingredients')
        r = requests.get(f'{url}/findByIngredients?apiKey={api_key}&{conditionals}&ingredients={ingredients}').json()
        for index, item in enumerate(r):
            titles.append(r[index]['title'])
            images.append(r[index]['image'])
            ids.append(r[index]['id'])
        items = zip(titles, images, ids)
        context = {'items': items}
        return render(request, 'recipes/recipes_from_ingredients.html', context)
    else:
        form = InsertIngredients()
        context = {'form': form}
        return render(request, 'recipes/insert_ingredients.html', context)


def requirements_recipes(request):
    context = {}
    return render(request, 'recipes/recipes_from_requirements.html', context)


