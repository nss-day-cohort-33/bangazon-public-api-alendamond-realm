from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Customer(models.Model):

    """
    Creates table for customer
    Author: Mary West
    methods: none
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=55)
    phone_number = models.CharField(max_length=55)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    # class Meta:
    #     ordering = (F('user.date_joined').asc(nulls_last=True),)