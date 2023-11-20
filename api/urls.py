from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name='api'),
    path('recipes-random/', views.recipes_random, name='recipes-random'),
    path('nutrients-list/', views.nutrients_list, name='nutrients-list'),
    path('recipes-ingredients/', views.recipes_ingredients, name='recipes-ingredients'),
]
