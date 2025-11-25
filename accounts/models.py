# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    dietary_preferences = models.TextField(blank=True, null=True)
    allergens = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} likes {self.recipe.name}"

class ShoppingListItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='shopping_list')
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255) 
    quantity = models.CharField(max_length=50, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True) 
    is_purchased = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.name}"


    