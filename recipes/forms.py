from django import forms


class InsertIngredients(forms.Form):
    ingredients = forms.CharField(max_length=150)
    fields = ['ingredients']


class InsertRequirements(forms.Form):
    minCalories = forms.CharField(max_length=5)
    maxCalories = forms.CharField(max_length=500)
    minProtein = forms.CharField(max_length=5)
    maxProtein = forms.CharField(max_length=5)
    minCarbs = forms.CharField(max_length=5)
    maxCarbs = forms.CharField(max_length=5)
    minFat = forms.CharField(max_length=5)
    maxFat = forms.CharField(max_length=5)
    fields = ['__all__']