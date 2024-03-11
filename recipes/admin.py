from django.contrib import admin
from .models import Nutrient, CustomRecipe, Ingredient, Step


admin.site.register(Nutrient)
admin.site.register(CustomRecipe)
admin.site.register(Ingredient)
admin.site.register(Step)