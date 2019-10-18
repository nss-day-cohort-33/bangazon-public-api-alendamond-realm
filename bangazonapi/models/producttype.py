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

    # @property
    # def total_sold(self):
    #     return self.orderproduct_set.filter(order__payment_type__isnull=False).count()

    @property
    def total_products(self):
        types = self.objects.all()
        for product_type in types:
            return self.product_set.filter(product_type=product_type).count()
        # return self.product.filter(product_type=self.product_type).count()

