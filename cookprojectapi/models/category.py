from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=25)
    recipe = models.ManyToManyField(
        'Recipe', 
        through="RecipeCategory",
        related_name="categories"
        )