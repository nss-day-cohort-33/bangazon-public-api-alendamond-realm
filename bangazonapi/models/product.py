from django.db import models
from .customer import Customer
from .producttype import ProductType


class Product(models.Model):
    """
    Creates table for product
    Author: Matthew McDevitt
    methods: none
    """
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    city = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(null=True, blank=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("product")
        verbose_name_plural = ("products")


    def __str__(self):
        return self.name
