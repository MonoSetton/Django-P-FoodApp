from django import forms
from django.forms import inlineformset_factory
from .models import CustomRecipe, Ingredient, Step


class InsertIngredients(forms.Form):
    ingredients = forms.CharField(max_length=150)
    fields = ['ingredients']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']


class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['body']


IngredientFormSet = inlineformset_factory(
    CustomRecipe, Ingredient, form=IngredientForm, extra=2, can_delete=False
)

StepFormSet = inlineformset_factory(
    CustomRecipe, Step, form=StepForm, extra=2, can_delete=False
)