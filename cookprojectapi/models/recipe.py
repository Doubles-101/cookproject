from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .customer import Customer

class Recipe(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=200)
    instructions = models.CharField(max_length=800)
    ingredients = models.CharField(max_length=300)
    time = models.IntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(15)
        ])
    customer = models.ForeignKey(Customer, related_name='recipes', on_delete=models.DO_NOTHING,)
