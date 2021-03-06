from django.db import models
from .customer import Customer
from safedelete.models import SOFT_DELETE
from safedelete.models import SafeDeleteModel



class PaymentType(SafeDeleteModel):

    """
    Created table for Payment Type
    Author: Joy Ittycheriah
    methods: none
    """

    _safedelete_policy = SOFT_DELETE
    merchant_name = models.CharField(max_length=25)
    acct_number = models.CharField(max_length=25)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    expiration_date = models.DateField()
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("paymenttype")
        verbose_name_plural = ("paymenttypes")

    def __str__(self):
        return self.merchant_name
