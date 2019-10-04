from django.db import models
from .order import Order
from .product import Product


class OrderProduct(models.Model):
    """
    Creates the join table for the many to many relationship between orders and products
    Author: Amber Gooch
    methods: none
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
