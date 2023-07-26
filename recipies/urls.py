from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipies_from_ingredients', views.ingredients_recipies, name='ingredients_recipies'),
    path('recipies_from_requirements', views.requirements_recipies, name='requirements_recipies'),
]
