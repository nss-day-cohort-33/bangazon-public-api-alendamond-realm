from django.db import models
from .customer import Customer



class Friend(models.Model):
    """
    Creates friend table
    Author: Matthew McDevitt
    methods: none
    """

    current = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="current")
    friend = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="friend")

