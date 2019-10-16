from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Order, Product, OrderProduct, Customer

# Author: Curt Cato
# Purpose: Allow a user to communicate with the Bangazon database to GET POST and DELETE order/product entries.
# Methods: GET POST DELETE


class ProductRatingSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for order/product join table

    Arguments:
        serializers
    """
    class Meta:
        model = ProductRating
        url = serializers.HyperlinkedIdentityField(
            view_name='productrating',
            lookup_field='id'
        )
        fields = ('id', 'customer_id', 'product_id', 'rating')
        depth = 2


class ProductRating(ViewSet):
    """Orders/Products for Bangazon"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized OrderProduct instance
        """
        new_productrating = ProductRating()
        new_productrating.product = Product.objects.get(pk=request.data["product_id"])
        new_productrating.customer = Customer.objects.get(pk=request.data["customer_id"])
        new_productrating.rating = request.data["rating"]

        new_productrating.save()

        serializer = ProductRatingSerializer(new_productrating, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single order/product relationship

        Returns:
            Response -- JSON serialized productrating instance
        """
        try:
            productrating = ProductRating.objects.get(pk=pk)
            serializer = ProductRatingSerializer(productrating, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product/customer relationship

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            productrating = ProductRating.objects.get(pk=pk)
            productrating.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProductRating.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to product types resource

        Returns:
            Response -- JSON serialized list of product types
        """
        ratings = ProductRating.objects.all()

        serializer = ProductRatingSerializer(
            ratings, many=True, context={'request': request})
        return Response(serializer.data)