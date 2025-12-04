# recipes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:id>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/<int:id>/delete/', views.recipe_delete, name='recipe_delete'),
    path('favorites/', views.favorites_view, name='favorites'),    
    path('toggle-favorite/<int:recipe_id>/', views.toggle_favorite, name='toggle_favorite'),    
    path('about/', views.about_view, name='about'),
    path('shopping-list/', views.shopping_list_view, name='shopping_list'),
    path('shopping-list/add-recipe/<int:recipe_id>/', views.add_recipe_ingredients_to_list, name='add_recipe_ingredients_to_list'),
    path('shopping-list/add-custom/', views.add_custom_shopping_item, name='add_custom_shopping_item'),
    path('shopping-list/delete/<int:item_id>/', views.delete_shopping_item, name='delete_shopping_item'),
    path('shopping-list/clear/', views.clear_all_shopping_items, name='clear_all_shopping_items'),
    path('reviews/', views.review_page, name='reviews'),
    path('shopping-list/toggle/<int:item_id>/', views.toggle_shopping_item_purchased, name='toggle_shopping_item_purchased'),
    path("api/recipe/<int:recipe_id>/rating-summary/", views.recipe_rating_summary),
    
]
