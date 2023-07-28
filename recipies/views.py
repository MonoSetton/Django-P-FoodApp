from django.shortcuts import render
import requests


api_key = '99aa443bda864d698ad5ac6db226c843'


def home(request):
    titles = []
    images = []
    url = "https://api.spoonacular.com/recipes/random"
    r = requests.get(f'{url}?tags=lunch&number=9&apiKey={api_key}')
    r = r.json()
    r = r['recipes']
    for index, item in enumerate(r):
        titles.append(r[index]['title'])
        if 'image' in r[index]:
            images.append(r[index]['image'])
        else:
            images.append()
    items = zip(titles, images)
    context = {'items': items}
    return render(request, 'recipies/home.html', context)


def ingredients_recipies(request):
    context = {}
    return render(request, 'recipies/recipies_from_ingredients.html', context)


def requirements_recipies(request):
    context = {}
    return render(request, 'recipies/recipies_from_requirements.html', context)


