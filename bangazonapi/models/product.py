from django.core.validators import MaxValueValidator, MinValueValidator
from safedelete.models import SOFT_DELETE
from safedelete.models import SafeDeleteModel
from django.db import models
from .customer import Customer
from .producttype import ProductType

class Product(SafeDeleteModel):
    """
    Creates table for product and method for calculating current inventory of a user's products.
    Author: Matthew McDevitt/Scott Silver
    methods: none
    """

    _safedelete_policy = SOFT_DELETE
    name = models.CharField(max_length=50)
    price = models.FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(10000.00)],)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    city = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("product")
        verbose_name_plural = ("products")

    @property
    def total_sold(self):
        return self.orderproduct_set.filter(order__payment_type__isnull=False).count()

    def __str__(self):
        return self.name
