# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('profile/', views.profile_view, name='profile'),   
    path('refresh-captcha/', views.refresh_captcha_view, name='refresh_captcha'), 
    path('favorites/', views.favorites_list, name='favorites'), 
    path('shopping-list/', views.shopping_list_view, name='shopping_list'),
    path('shopping-list/add-recipe/<int:recipe_id>/', views.add_recipe_ingredients_to_list, name='add_recipe_ingredients_to_list'),
    path('shopping-list/add-custom/', views.add_custom_item, name='add_custom_item'),
    path('shopping-list/delete/<int:item_id>/', views.delete_shopping_item, name='delete_shopping_item'),
    path('shopping-list/clear/', views.clear_shopping_list, name='clear_shopping_list'),
    path('shopping-list/toggle/<int:item_id>/', views.toggle_purchased, name='toggle_purchased'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('create/', views.create_recipe, name='create_recipe'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('dashboard/', views.profile_view, name='profile_dashboard'),
    path('clear-purchased/', views.clear_purchased_items, name='clear_purchased'),    
]