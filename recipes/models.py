from django.db import models


class Nutrient(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class ForeignAPI(models.Model):
    name = models.CharField(max_length=50, default='API Name')
    API_key = models.CharField(max_length=150)
    url = models.CharField(max_length=150)

    def __str__(self):
        return self.name