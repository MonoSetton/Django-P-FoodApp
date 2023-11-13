from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('detail_recipes/<str:pk>', views.detail_recipes, name='detail_recipes'),
    path('insert_requirements', views.requirements_recipes, name='insert_requirements'),
]
