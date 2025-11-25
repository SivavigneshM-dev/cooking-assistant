from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('veg', 'Veg'),
        ('non-veg', 'Non-Veg'),
    ]
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]
    RECIPE_TYPE_CHOICES = [
        ('sweet', 'Sweet'),
        ('meals', 'Meals'),
        ('side', 'Side Dish'),
        ('snacks', 'Snacks'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    name = models.CharField(max_length=200)
    short_description = models.TextField() 
    instructions = models.TextField()      
    image = models.ImageField(upload_to='recipes/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    meal_time = models.CharField(max_length=20, choices=MEAL_CHOICES)
    recipe_type = models.CharField(max_length=20, choices=RECIPE_TYPE_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE) 

    cook_time = models.CharField(
        max_length=50, 
        help_text="e.g., '25 min', '1 hr 15 min'"
    )
    servings = models.IntegerField(
        default=4,
        help_text="Number of people this recipe serves"
    )
    difficulty = models.CharField(
        max_length=20, 
        choices=DIFFICULTY_CHOICES,
        default='easy'
    )
    cuisine = models.CharField(
        max_length=100, 
        help_text="e.g., 'Mediterranean', 'Indian', 'Italian'"
    )

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    # This model is correct and handles your ingredients list
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients_list')
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50, help_text="e.g., '1 cup', '2 large', '1 tsp'")
    
    def __str__(self):
        return f"{self.quantity} of {self.name}"

class Instruction(models.Model):
    # Links instruction step back to the primary Recipe
    recipe = models.ForeignKey(
        'Recipe', # Use string reference if Recipe is defined above, or just Recipe
        on_delete=models.CASCADE, 
        related_name='instructions_steps'
    ) 
    step_number = models.IntegerField()
    description = models.TextField() 

    def __str__(self):
        return f"Step {self.step_number} for {self.recipe.name}"