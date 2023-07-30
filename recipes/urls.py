from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detail_recipes/<str:pk>', views.detail_recipes, name='detail_recipes'),
    path('insert_ingredients', views.ingredients_recipes, name='insert_ingredients'),
    path('insert_requirements', views.requirements_recipes, name='insert_requirements'),
]
