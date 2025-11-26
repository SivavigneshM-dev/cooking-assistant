# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import SimpleSignupForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from . models import UserProfile, Favorite, ShoppingListItem
from recipes.models import Recipe, Ingredient, Instruction




def signup_view(request):
    if request.method == 'POST':
        form = SimpleSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SimpleSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("/")

def register_view(request):
    return render(request, 'accounts/register.html', {})

def forgot_password_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user_answer = request.POST.get('captcha_answer')
        new_pass = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')
        expected_sum = request.session.get('captcha_sum')
        
        if not expected_sum or int(user_answer) != expected_sum:
            messages.error(request, "Incorrect math answer. Please try again.")
            return redirect('forgot_password')

        if new_pass != confirm_pass:
            messages.error(request, "Passwords do not match.")
            return redirect('forgot_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_pass)
            user.save()
            messages.success(request, "Password reset successfully! Please login.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "User with that username does not exist.")
            return redirect('forgot_password')
    else:
        num1 = random.randint(10, 99)
        num2 = random.randint(10, 99)
        request.session['captcha_sum'] = num1 + num2
        context = {'num1': num1, 'num2': num2}
        return render(request, 'accounts/forgot_password.html', context)

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {'u_form': u_form, 'active_tab': 'profile'}
    return render(request, 'accounts/profile.html', context)

def refresh_captcha_view(request):
    num1 = random.randint(10, 99)
    num2 = random.randint(10, 99)
    request.session['captcha_sum'] = num1 + num2      
    return JsonResponse({'num1': num1, 'num2': num2})

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('recipe')
    recipes = [favorite.recipe for favorite in favorites]    
    context = {'recipes': recipes}
    return render(request, 'accounts/favorites.html', context)

@login_required
def shopping_list_view(request):
    items = ShoppingListItem.objects.filter(user=request.user).order_by('recipe__name', 'added_at')
    context = {'shopping_list_items': items, 'active_tab': 'shopping_list'}
    return render(request, 'accounts/shopping_list.html', context)

@login_required
@require_POST # <--- ADD THIS DECORATOR
def add_recipe_ingredients_to_list(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    # The 'if request.method == 'POST':' block is now redundant and can be removed
    
    recipe_ingredients = recipe.ingredients_list.all() 
    items_added = 0
    for ingredient in recipe_ingredients:
        # ... (rest of your ShoppingListItem creation logic) ...
        ShoppingListItem.objects.create(
            user=request.user,
            recipe=recipe,
            name=ingredient.name,
            quantity=ingredient.quantity,
            # unit=ingredient.unit
        )
        items_added += 1
        
    messages.success(request, f"Successfully added {items_added} ingredients from '{recipe.name}' to your shopping list.")
    return redirect('shopping_list')
    # return redirect('my_recipes') 

@login_required
def add_custom_item(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        if item_name:
            ShoppingListItem.objects.create(
                user=request.user,
                name=item_name,
                recipe=None 
            )
    return redirect('shopping_list')

@login_required
def delete_shopping_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ShoppingListItem, id=item_id, user=request.user)
        item.delete()
        messages.info(request, "Item removed from list.")
    return redirect('shopping_list')

@login_required
def clear_shopping_list(request):
    ShoppingListItem.objects.filter(user=request.user).delete()
    messages.success(request, "Shopping list cleared.")
    return redirect('shopping_list')

@login_required
def toggle_purchased(request, item_id):
    item = get_object_or_404(ShoppingListItem, id=item_id, user=request.user)
    item.is_purchased = not item.is_purchased
    item.save()
    return redirect('shopping_list')

@login_required
def add_recipe(request):
    if request.method == 'POST':
        # 1. Save Basic Recipe Info
        # FIXED: mapped form fields to correct Model fields (user, name)
        recipe = Recipe.objects.create(
            user=request.user,
            name=request.POST.get('title'), 
            description=request.POST.get('description'),
            image_url=request.POST.get('image_url'),
            category=request.POST.get('category'),
            difficulty=request.POST.get('difficulty'),
            cook_time=request.POST.get('cook_time'),
            servings=request.POST.get('servings'),
        )

        # 2. Handle Ingredients List
        names = request.POST.getlist('ingredient_name[]')
        amounts = request.POST.getlist('ingredient_amount[]')
        units = request.POST.getlist('ingredient_unit[]')

        for i in range(len(names)):
            if names[i].strip():
                Ingredient.objects.create(
                    recipe=recipe,
                    name=names[i],
                    amount=amounts[i], # This now matches the model
                    unit=units[i]      # This now matches the model
                )

        # 3. Handle Instructions Steps
        steps = request.POST.getlist('instructions[]')
        for index, step_desc in enumerate(steps):
            if step_desc.strip():
                Instruction.objects.create(
                    recipe=recipe,
                    step_number=index + 1,
                    description=step_desc # This now matches the model
                )

        return redirect('my_recipes') 

    return render(request, 'accounts/add_recipe.html')

@login_required
def create_recipe(request):
    # This seems redundant with add_recipe, but kept to prevent URL crash
    return render(request, 'accounts/create_recipe.html')

@login_required
def my_recipes(request):
    # THIS WAS MISSING
    recipes = Recipe.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/my_recipes.html', {'recipes': recipes})



@login_required
def clear_purchased_items(request):
    """Deletes all items in the shopping list that are marked as purchased."""
    if request.method == 'GET':
        # Filter items belonging to the current user that are marked as purchased
        purchased_items = ShoppingListItem.objects.filter(
            user=request.user, 
            is_purchased=True
        )
        count = purchased_items.count()
        purchased_items.delete()
        
        if count > 0:
            messages.success(request, f'Successfully cleared {count} purchased items!')
        else:
            messages.info(request, 'No purchased items to clear.')
            
    # Redirect back to the shopping list page
    return redirect('shopping_list')