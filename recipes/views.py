from django.shortcuts import render, redirect
from .forms import InsertIngredients, IngredientFormSet, StepFormSet
import requests
from django.contrib.auth.decorators import login_required
from .models import Nutrient, ForeignAPI, CustomRecipe, Ingredient, Step


spoonacular = ForeignAPI.objects.get(name='Spoonacular')
api_key = spoonacular.API_key
url = spoonacular.url


@login_required(login_url='/login')
def home(request):
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
    form = InsertIngredients()
    context = {'items': items, 'form': form}
    return render(request, 'recipes/home.html', context)


@login_required(login_url='/login')
def detail_recipes(request, pk):
    r = requests.get(f'{url}/{pk}/information?apiKey={api_key}&'
                     f'includeNutrition=false').json()
    sourceURL = r['sourceUrl']
    return redirect(sourceURL)


@login_required(login_url='/login')
def requirements_recipes(request):
    nutrients = Nutrient.objects.all()
    context = {'nutrients': nutrients}
    return render(request, 'recipes/insert_requirements.html', context)


@login_required(login_url='/login')
def custom_recipes(request):
    if request.method == 'POST':
        ingredient_formset = IngredientFormSet(request.POST, prefix='ingredient')
        step_formset = StepFormSet(request.POST, prefix='step')
        if ingredient_formset.is_valid() and step_formset.is_valid():
            ingredients = ingredient_formset.save(commit=False)
            steps = step_formset.save(commit=False)

            recipe = CustomRecipe.objects.create(name=request.POST.get('name'), author=request.user)

            for ingredient in ingredients:
                ingredient.recipe = recipe
                ingredient.save()

            for step in steps:
                step.recipe = recipe
                step.save()

            return redirect('profile')
    else:
        ingredient_formset = IngredientFormSet(prefix='ingredient')
        step_formset = StepFormSet(prefix='step')

    return render(request, 'recipes/create_custom_recipe.html', {
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
    })


@login_required(login_url='/login')
def detail_custom_recipe(request, pk):
    recipe = CustomRecipe.objects.get(id=pk)
    ingredients = Ingredient.objects.filter(recipe=recipe)
    steps = Step.objects.filter(recipe=recipe)
    context = {'recipe': recipe, 'ingredients': ingredients, 'steps': steps}
    return render(request, 'recipes/detail_custom_recipe.html', context)