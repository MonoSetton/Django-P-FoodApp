from django.shortcuts import render, redirect
from .forms import InsertIngredients, InsertRequirements
import requests


api_key = '99aa443bda864d698ad5ac6db226c843'
url = "https://api.spoonacular.com/recipes"


def home(request):
    titles, images, ids, readyInMinutes, servings = [], [], [], [], []
    r = requests.get(f'{url}/random?apiKey={api_key}&tags=lunch&number=9').json()
    r = r['recipes']
    for index, item in enumerate(r):
        if 'image' in r[index]:
            titles.append(r[index]['title'])
            images.append(r[index]['image'])
            ids.append(r[index]['id'])
            readyInMinutes.append(r[index]['readyInMinutes'])
            servings.append(r[index]['servings'])
    items = zip(titles, images, ids, readyInMinutes, servings)
    context = {'items': items}
    return render(request, 'recipes/home.html', context)


def detail_recipes(request, pk):
    r = requests.get(f'{url}/{pk}/information?apiKey={api_key}&'
                     f'includeNutrition=false').json()
    sourceURL = r['sourceUrl']
    return redirect(sourceURL)


def ingredients_recipes(request):
    if request.method == 'POST':
        titles, images, ids = [], [], []
        conditionals = 'number=6&ranking=1&ignorePantry=false'
        ingredients = request.POST.get('ingredients')
        r = requests.get(f'{url}/findByIngredients?apiKey={api_key}&'
                         f'{conditionals}&'
                         f'ingredients={ingredients}').json()
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
    if request.method == 'POST':
        titles, images, ids = [], [], []
        r = requests.get(f'{url}/findByNutrients?apiKey={api_key}&'
                         f'minCarbs={request.POST.get("minCarbs")}&maxCarbs={request.POST.get("maxCarbs")}&'
                         f'minProtein={request.POST.get("minProtein")}&maxProtein={request.POST.get("maxProtein")}&'
                         f'minCalories={request.POST.get("minCalories")}&maxCalories={request.POST.get("maxCalories")}&'
                         f'minFat={request.POST.get("minFat")}&maxFat={request.POST.get("maxFat")}&'
                         f'number=9&random=true').json()
        for index, item in enumerate(r):
            titles.append(r[index]['title'])
            images.append(r[index]['image'])
            ids.append(r[index]['id'])
        items = zip(titles, images, ids)
        context = {'items': items}
        return render(request, 'recipes/recipes_from_requirements.html', context)
    else:
        form = InsertRequirements()
        context = {'form': form}
        return render(request, 'recipes/insert_requirements.html', context)


