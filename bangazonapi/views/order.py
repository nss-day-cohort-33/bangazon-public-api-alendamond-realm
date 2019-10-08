"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import *


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for orders

    Arguments:
        serializers
    """

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'payment_type_id', 'customer_id', 'created_at')
        depth = 2


class Orders(ViewSet):
    """Order items for Bangazon customers"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized order instance
        """
        new_order = Order()
        new_order.customer = Customer.objects.get(user=request.auth.user)
        new_order.payment_type = PaymentType.objects.get(pk=request.data["payment_type_id"])
        new_order.created_at = request.data["created_at"]

        new_order.save()

        serializer = OrderSerializer(new_order, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single order

        Returns:
            Response -- JSON serialized order instance
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area itinerary

        Returns:
            Response -- Empty body with 204 status code
        """
        order = Order.objects.get(pk=pk)
        order.created_at = request.data["created_at"]
        order.payment_type_id = PaymentType.objects.get(pk=request.data["payment_type_id"])
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a order are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order = Order.objects.get(pk=pk)
            order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to orders resource

        Returns:
            Response -- JSON serialized list of orders
        """
        customer = Customer.objects.get(user=request.auth.user)
        orders = Order.objects.filter(customer=customer)
        # orders = Order.objects.all()


        serializer = OrderSerializer(
            orders, many=True, context={'request': request})
        return Response(serializer.data)
