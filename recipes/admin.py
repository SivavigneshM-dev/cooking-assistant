from django.contrib import admin
from .models import Recipe, Ingredient 

class IngredientInline(admin.TabularInline):
    model = Ingredient
    fields = ['name', 'quantity']
    extra = 3 

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'meal_time', 'recipe_type', 'created_by') 
    
    list_display_links = ('id', 'name')
    
    list_filter = ('category', 'meal_time', 'recipe_type')
    search_fields = ('name', 'short_description')
    
    inlines = [IngredientInline] 

    fields = (
        'name',
        'short_description',
        'instructions',
        'image',
        'category',
        'meal_time',
        'recipe_type',
        'created_by', 
        'cook_time', 
        'servings',
        'difficulty',
        'cuisine',
    )
    
    readonly_fields = ('created_by',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
