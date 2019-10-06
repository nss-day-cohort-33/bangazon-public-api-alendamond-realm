"""View module for handling requests about customers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from bangazonapi.models import Customer



class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Customers
    Arguments:
        serializers
    """

    users = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        view_name="user-detail",
        many=False,
        required=False,
        lookup_field="pk"
    )
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'url', 'phone_number', 'address', 'user_id','users')
        depth = 1

class Customers(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Attraction instance
        """
        new_customer = Customer()
        new_customer.address = request.data["address"]
        new_customer.phone_number = request.data["phone_number"]
        new_customer.user_id = request.data["user_id"]
        new_customer.save()

        serializer = CustomerSerializer(new_customer, context={'request': request})

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


    def list(self, request):
        customers = Customer.objects.all()

        user_id = self.request.query_params.get('customer', None)
        if user_id is not None:
            customers = customers.filter(user_id=user_id)

        serializer = CustomerSerializer(
            customers, many=True, context={'request': request})
        return Response(serializer.data)



