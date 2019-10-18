from django.db import models

class ProductType(models.Model):

    """
    Creates table for product types
    Author: Amber Gooch
    methods: none
    """

    name = models.CharField(max_length = 55)

    class Meta:
        verbose_name = ("producttype")
        verbose_name_plural = ("producttypes")

    def __str__(self):
        return self.name

    @property
    def total_products(self):
        return self.product_set.filter(product_type=self.id).count()

