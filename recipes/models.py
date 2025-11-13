from django.db import models



class Recipe(models.Model):
    FOOD_TYPE_CHOICES = [
        ('Veg', 'Veg'),
        ('Non-Veg', 'Non-Veg'),
    ]
    MEAL_TIME_CHOICES = [
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Evening', 'Evening'),
    ]
    OCCASION_CHOICES = [
        ('Regular', 'Regular'),
        ('Special', 'Special'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    instructions = models.TextField()
    food_type = models.CharField(max_length=20, choices=FOOD_TYPE_CHOICES)
    meal_time = models.CharField(max_length=20, choices=MEAL_TIME_CHOICES)
    occasion_type = models.CharField(max_length=20, choices=OCCASION_CHOICES)
    prep_time = models.PositiveIntegerField(help_text="Time in minutes")

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.quantity})"
