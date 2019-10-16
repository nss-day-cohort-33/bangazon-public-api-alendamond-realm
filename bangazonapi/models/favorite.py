from django.db import models
from .customer import Customer



class Favorite(models.Model):
    """
    Creates friend table
    Author: Matthew McDevitt
    methods: none
    """

    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="buyer" )
    seller = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="seller")

