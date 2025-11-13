from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, RecipeIngredient
from .forms import RecipeForm, RecipeIngredientFormSet


def recipe_list(request):
    food_type_filter = request.GET.get('food_type')
    page_title = "All Recipes"

    if food_type_filter == 'veg':
        recipes = Recipe.objects.filter(food_type='veg')
        page_title = "Veg Recipes"
    elif food_type_filter == 'non-veg':
        recipes = Recipe.objects.filter(food_type='non-veg')
        page_title = "Non-Veg Recipes"
    else:
        recipes = Recipe.objects.all()

    context = {
        'recipes_list': recipes,
        'page_title': page_title,
    }
    return render(request, 'recipes.html', context)


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    context = {
        'recipe': recipe,
        'ingredients': ingredients,
    }
    return render(request, 'recipe_detail.html', context)


def add_recipe_view(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        formset = RecipeIngredientFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            ingredients = formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = recipe
                ingredient.save()
            return redirect('recipes:recipe_list')
    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet()

    context = {
        'form': form,
        'formset': formset
    }
    return render(request, 'add_recipe.html', context)
