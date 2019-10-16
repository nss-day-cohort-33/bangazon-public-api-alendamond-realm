from django.db import models
from .customer import Customer
from .product import Product


class LikeDislike(models.Model):
    """
    Creates the like and dislike table
    Author: Matthew McDevitt
    methods: none
    """

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    like_dislike = models.BinaryField()

