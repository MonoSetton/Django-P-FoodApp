from django.db import models
from django.contrib.auth.models import User


class Nutrient(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class CustomRecipe(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(null=True, blank=True, upload_to='recipe_images')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=75)
    recipe = models.ForeignKey(CustomRecipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Step(models.Model):
    body = models.CharField(max_length=350)
    recipe = models.ForeignKey(CustomRecipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.body

