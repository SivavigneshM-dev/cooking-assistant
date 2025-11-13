from django.contrib import admin
from .models import Ingredient ,Recipe , RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ('name', 'food_type', 'meal_time', 'occasion_type', 'prep_time')
    list_filter = ('food_type', 'meal_time', 'occasion_type')

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)