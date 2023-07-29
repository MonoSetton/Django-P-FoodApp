from django import forms


class InsertIngredients(forms.Form):
    ingredients = forms.CharField(max_length=150)
    fields = ['ingredients']
