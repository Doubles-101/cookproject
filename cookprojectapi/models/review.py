from django.db import models
from .customer import Customer
from .recipe import Recipe

class Review(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer', on_delete=models.DO_NOTHING,)
    recipe = models.ForeignKey(Recipe, related_name='recipe', on_delete=models.DO_NOTHING,)
    comment = models.CharField(max_length=300)
    create_date = models.DateField(default="0000-00-00",)