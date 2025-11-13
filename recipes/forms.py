from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient,
    fields=('name', 'quantity'),
    extra=1,
    can_delete=True
)
