from django.shortcuts import render


def home(request):
    context = {}
    return render(request, 'recipies/home.html', context)


def ingredients_recipies(request):
    context = {}
    return render(request, 'recipies/recipies_from_ingredients.html', context)


def requirements_recipies(request):
    context = {}
    return render(request, 'recipies/recipies_from_requirements.html', context)


