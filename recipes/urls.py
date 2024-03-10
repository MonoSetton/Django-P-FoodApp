from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.home),
    path('detail_recipes/<str:pk>', views.detail_recipes, name='detail_recipes'),
    path('insert_requirements', views.requirements_recipes, name='insert_requirements'),
    path('custom_recipes/', views.custom_recipes, name='custom_recipes'),
    path('detail_custom_recipe/<str:pk>', views.detail_custom_recipe, name='detail_custom_recipe'),
    path('delete_custom_recipe/<str:pk>', views.delete_custom_recipe, name='delete_custom_recipe'),
    path('update_custom_recipe/<str:pk>', views.update_custom_recipe, name='update_custom_recipe'),
]
