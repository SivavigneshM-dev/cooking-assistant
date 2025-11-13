from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, RecipeIngredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'name', 
            'description', 
            'instructions', 
            'food_type', 
            'meal_time', 
            'occasion_type', 
            'prep_time'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'food_type': forms.Select(attrs={'class': 'form-select'}),
            'meal_time': forms.Select(attrs={'class': 'form-select'}),
            'occasion_type': forms.Select(attrs={'class': 'form-select'}),
            'prep_time': forms.NumberInput(attrs={'class': 'form-control'}),
        }


RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    fields=('ingredient', 'quantity'),
    extra=1,
    can_delete=True
)
