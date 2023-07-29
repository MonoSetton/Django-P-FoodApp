from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes_from_ingredients', views.ingredients_recipes, name='ingredients_recipes'),
    path('recipes_from_requirements', views.requirements_recipes, name='requirements_recipes'),
    path('detail_recipes/<str:pk>', views.detail_recipes, name='detail_recipes'),
    path('insert_ingredients', views.ingredients_recipes, name='insert_ingredients'),
]
