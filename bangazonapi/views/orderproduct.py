"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Order, Product, OrderProduct


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for order/product join table

    Arguments:
        serializers
    """
    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='orderproduct',
            lookup_field='id'
        )
        fields = ('id', 'order_id', 'product_id')
        depth = 2


class OrdersProducts(ViewSet):
    """Orders/Products for Bangazon"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized OrderProduct instance
        """
        new_orderproduct = OrderProduct()
        new_orderproduct.order = Order.objects.get(pk=request.data["order_id"])
        new_orderproduct.product = Product.objects.get(pk=request.data["product_id"])

        new_orderproduct.save()

        serializer = OrderProductSerializer(new_orderproduct, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single order/product relationship

        Returns:
            Response -- JSON serialized OrderProduct instance
        """
        try:
            orderproduct = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(orderproduct, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single order/product relationship

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            orderproduct = OrderProduct.objects.get(pk=pk)
            orderproduct.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except OrderProduct.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to product types resource

        Returns:
            Response -- JSON serialized list of product types
        """
        items = OrderProduct.objects.all()

        serializer = OrderProductSerializer(
            items, many=True, context={'request': request})
        return Response(serializer.data)


