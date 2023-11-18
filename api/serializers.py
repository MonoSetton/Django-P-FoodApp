from rest_framework import serializers
from recipes.models import Nutrient


class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fields = '__all__'



