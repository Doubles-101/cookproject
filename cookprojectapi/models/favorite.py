from django.db import models
from .customer import Customer
from .recipe import Recipe

class Favorite(models.Model):
    customer = models.ForeignKey(Customer, related_name='favorites', on_delete=models.DO_NOTHING,)
    recipe = models.ForeignKey(Recipe, related_name='favorite_by', on_delete=models.DO_NOTHING,)