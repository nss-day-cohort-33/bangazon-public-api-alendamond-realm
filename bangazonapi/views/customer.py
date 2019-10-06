"""View module for handling requests about customers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from bangazonapi.models import Customer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'user_id', 'email')

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customers

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
        )
        fields = ('id', 'url', 'user_id', 'address', 'phone_number')
        depth = 1


class Customers(ViewSet):
    """Customers for Bangazon Galaydia Empire"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Customer instance
        """
        newcustomer = Customer()
        newcustomer.address = request.data["address"]
        newcustomer.phone_number = request.data["phone_number"]
        newcustomer.save()

        serializer = CustomerSerializer(newcustomer, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer

        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)