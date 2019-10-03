from django.db import models
from django.urls import reverse

class Customer(models.Model):

    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=55)
    username = models.CharField(max_length=55)
    address = models.CharField(max_length=55)
    phone_number = models.IntegerField()
    created_at = models.DateField()
    is_active = models.BooleanField()


    class Meta:
        verbose_name = ("Customer")
        verbose_name_plural = ("Customers")

    def get_absolute_url(self):
        return reverse("customer_details", kwargs={"pk": self.pk})