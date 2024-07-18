from django.db import models

class RecipeImage(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name="recipe_image")
    recipe_pic = models.ImageField(
        upload_to='recipeimages', height_field=None,
        width_field=None, max_length=None, null=True)