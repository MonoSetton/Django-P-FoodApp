from django.contrib import admin
from .models import Nutrient, ForeignAPI, CustomRecipe, Ingredient, Step


admin.site.register(Nutrient)
admin.site.register(ForeignAPI)
admin.site.register(CustomRecipe)
admin.site.register(Ingredient)
admin.site.register(Step)