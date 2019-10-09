from django.db import models
from .customer import Customer
from .paymenttype import PaymentType

## Purpose: Joins customer and payment type tables
## Author: Curt Cato

class Order(models.Model):

    """
    Creates table for orders
    Author: Curt Cato
    methods: none
    """

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = ("order")
        verbose_name_plural = ("orders")

    def __str__(self):
        return f'{self.customer.user.first_name} uses {self.payment_type.merchant_name}'