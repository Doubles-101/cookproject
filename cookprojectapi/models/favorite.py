from django.db import models
from .customer import Customer
from .recipe import Recipe

class Favorite(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer', on_delete=models.DO_NOTHING,)
    recipe = models.ForeignKey(Recipe, related_name='recipe', on_delete=models.DO_NOTHING,)