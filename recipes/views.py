from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
from .forms import RecipeForm
from .models import Recipe, Ingredient 
from accounts.models import Favorite
from accounts.models import ShoppingListItem
from django.http import JsonResponse
from django.db.models import Avg, Count
from . import models


def home(request):
    recipes = Recipe.objects.all()

    category = request.GET.get("category")
    meal_time = request.GET.get("meal_time")
    recipe_type = request.GET.get("recipe_type")

    if category:
        recipes = recipes.filter(category=category)
    if meal_time:
        recipes = recipes.filter(meal_time=meal_time)
    if recipe_type:
        recipes = recipes.filter(recipe_type=recipe_type)
        
    if request.user.is_authenticated:
        favorite_recipes_ids = Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)
        for recipe in recipes:
            recipe.is_favorite = recipe.id in favorite_recipes_ids
    else:
        for recipe in recipes:
            recipe.is_favorite = False 

    return render(request, "recipes/home.html", {"recipes": recipes})


@login_required
def favorite_toggle(request, recipe_id):
    return redirect('/') 

@login_required(login_url='/accounts/signup/')
def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    ingredients = recipe.ingredients_list.all() 
    
    if recipe.instructions:
        instructions_list = [step.strip() for step in recipe.instructions.split('\n') if step.strip()]
    else:
        instructions_list = []
    
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, recipe_id=recipe.id).exists()

    context = {
        "recipe": recipe,
        "ingredients": ingredients,        
        "instructions_list": instructions_list,
        "is_favorite": is_favorite, 
    }
    
    return render(request, "recipes/recipe_detail.html", context)

@login_required
def recipe_edit(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    if request.user != recipe.created_by:
        return redirect("/")

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect(f"/recipe/{id}/")
    else:
        form = RecipeForm(instance=recipe)

    return render(request, "recipes/recipe_edit.html", {"form": form})

@login_required
def recipe_delete(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    if request.user != recipe.created_by:
        return redirect("/")

    if request.method == "POST":
        recipe.delete()
        return redirect("/")

    return render(request, "recipes/recipe_delete.html")

@login_required
def favorites_view(request):
    if request.user.is_authenticated:
        favorite_entries = Favorite.objects.filter(user=request.user).select_related('recipe')
        favorite_recipes = [entry.recipe for entry in favorite_entries]
    else:
        favorite_recipes = []
        
    context = {'recipes': favorite_recipes} 
    return render(request, 'recipes/favorites.html', context)

def about_view(request):
    """Renders the About page."""
    return render(request, 'about.html')


@login_required(login_url='/accounts/login/')
def toggle_favorite(request, recipe_id):
    """
    Handles the Heart Button Click via AJAX
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    
    favorite_item = Favorite.objects.filter(user=request.user, recipe=recipe).first()
    
    data = {}

    if favorite_item:
        favorite_item.delete()
        data['status'] = 'removed'
        data['message'] = 'Removed from favorites'
    else:
        Favorite.objects.create(user=request.user, recipe=recipe)
        data['status'] = 'added'
        data['message'] = 'Added to favorites'

    return JsonResponse(data)
    # return redirect(request.META.get('HTTP_REFERER', 'default_url_name'))






@login_required
def shopping_list_view(request):
    items = ShoppingListItem.objects.filter(user=request.user).order_by('added_at')
    context = {'shopping_list_items': items}
    return render(request, 'shopping_list.html', context)

@login_required
def add_recipe_ingredients_to_list(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        ingredients = recipe.ingredients_list.all()

        for ingredient in ingredients:

            ShoppingListItem.objects.create(
                user=request.user,
                name=ingredient.name,
                quantity=ingredient.quantity,
                unit="",
                is_purchased=False,
            )
        return redirect('shopping_list')
    return redirect('recipe_detail',id=recipe_id)


@login_required
def add_custom_shopping_item(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        if item_name:
            ShoppingListItem.objects.create(user=request.user, name=item_name)
        return redirect('shopping_list')
    return redirect('shopping_list')

@login_required
def delete_shopping_item(request, item_id):
    item = get_object_or_404(ShoppingListItem, id=item_id, user=request.user)
    item.delete()
    return redirect('shopping_list')

@login_required
def clear_all_shopping_items(request):
    if request.method == 'POST':
        ShoppingListItem.objects.filter(user=request.user).delete()
    return redirect('shopping_list')

@login_required
def toggle_shopping_item_purchased(request, item_id):
    item = get_object_or_404(ShoppingListItem, id=item_id, user=request.user)
    item.is_purchased = not item.is_purchased
    item.save()
    return redirect('shopping_list')

@login_required
def review_page(request):
    """
    Renders the 'review.html' template.
    Ensure 'review.html' is located in 'recipes/templates/recipes/' 
    or just 'recipes/templates/'.
    """
    return render(request, 'recipes/review.html', {})



def recipe_rating_summary(request, recipe_id):
    recipe = get_object_or_404(models.Recipe, id=recipe_id)
    qs = recipe.reviews.filter(is_deleted=False)


    # counts
    counts = qs.values("rating").annotate(c=Count("rating"))
    counter = {1:0,2:0,3:0,4:0,5:0}

    for item in counts:
        counter[item["rating"]] = item["c"]

    total = qs.count()
    avg = qs.aggregate(a=Avg("rating"))["a"] or 0

    return JsonResponse({
        "avg": round(avg, 2),
        "total": total,
        "stars": counter
    })
