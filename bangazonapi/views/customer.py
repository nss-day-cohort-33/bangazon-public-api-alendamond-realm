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

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'url', 'user', 'phone_number', 'address', 'user_id')
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

        user = Customer.objects.get(user=request.auth.user)
        new_customer.user = user
        new_customer.save()

        serializer = CustomerSerializer(new_customer, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a single payment type

        Returns:
            Response -- Empty body with 204 status code
        """
        update_customer = Customer.objects.get(pk=pk)

        user = User.objects.get(pk=request.data["user_id"])

        update_customer.address = request.data["address"]
        update_customer.phone_number = request.data["phone_number"]

        update_customer.user = user
        update_customer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a order are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            customer = Customer.objects.get(pk=pk)
            customer.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Customer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

        # user_id = self.request.query_params.get('customer', None)
        # if user_id is not None:
        #     customers = customers.filter(user_id=user_id)



        serializer = CustomerSerializer(
            customers, many=True, context={'request': request})
        return Response(serializer.data)

