from django.shortcuts import render, redirect
import requests


api_key = '99aa443bda864d698ad5ac6db226c843'


def home(request):
    titles = []
    images = []
    ids = []
    url = "https://api.spoonacular.com/recipes/random"
    r = requests.get(f'{url}?apiKey={api_key}&tags=lunch&number=9')
    r = r.json()
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
    url = 'https://api.spoonacular.com/recipes/'
    r = requests.get(f'{url}/{pk}/information?apiKey={api_key}&includeNutrition=false')
    r = r.json()
    sourceURL = r['sourceUrl']
    return redirect(sourceURL)


def ingredients_recipes(request):
    context = {}
    return render(request, 'recipes/recipes_from_ingredients.html', context)


def requirements_recipes(request):
    context = {}
    return render(request, 'recipes/recipes_from_requirements.html', context)


