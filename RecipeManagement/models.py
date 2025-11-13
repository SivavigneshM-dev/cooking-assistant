from django.db import models
from django.contrib.auth.models import User 


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    

    FOOD_TYPE_CHOICES = [
        ('veg', 'Veg'),
        ('non-veg', 'Non-Veg'),
    ]
    
    MEAL_TIME_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('night', 'Night'),
    ]
    
    OCCASION_TYPE_CHOICES = [
        ('school/office', 'School/Office'),
        ('festival', 'Festival'),
        ('relatives', 'Relatives'),
        ('regular', 'Regular'),
    ]


    name = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()

    food_type = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICES, default='veg')
    meal_time = models.CharField(max_length=20, choices=MEAL_TIME_CHOICES, default='afternoon')
    occasion_type = models.CharField(max_length=20, choices=OCCASION_TYPE_CHOICES, default='regular')
    prep_time = models.PositiveIntegerField(help_text="Time in minutes") 
    

    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient') 

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE) 
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE) 
    
    
    quantity = models.CharField(max_length=100, help_text="e.g., '100g', '2', '1 tsp'") 
    
    def __str__(self):
        return f"{self.recipe.name} - {self.ingredient.name} ({self.quantity})"