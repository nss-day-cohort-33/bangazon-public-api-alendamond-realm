from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import *

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products
        Arguments:
        serializers.HyperlinkedModelSerializer
    """
    product_type = serializers.HyperlinkedRelatedField(
        queryset=ProductType.objects.all(),
        view_name="producttype-detail",
        many=True,
        required=False,
        lookup_field="pk"
    )

    customer = serializers.HyperlinkedRelatedField(
        queryset=Customer.objects.all(),
        view_name="customer-detail",
        many=True,
        required=False,
        lookup_field="pk"
    )

    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
        view_name='product',
        lookup_field='id'
        )

        fields = ('id', 'url', 'name', 'price', 'description', 'quantity',
        'city', 'created_at', 'image', 'product_type', 'customer')
        depth = 1


class ProductData(ViewSet):
    """Handle POST operations
        Returns:
            Response -- JSON serialized product instance
        """
    def create(self, request):
        new_product = Product()
        new_product.customer = Customer.objects.get(user=request.auth.user)
        new_product.product_type = ProductType.objects.get(pk=request.data['product_type'])
        new_product.name = request.data["name"]
        new_product.price = request.data["price"]
        new_product.description = request.data['description']
        new_product.quantity = request.data['quantity']
        new_product.city = request.data['city']
        new_product.created_at = request.data['created_at']
        new_product.image = request.data['image']
        new_product.save()
        serializer = ProductSerializer(new_product, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area
        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area
        Returns:
            Response -- Empty body with 204 status code
        """
        product = Product.objects.get(pk=pk)
        product.name = request.data["name"]
        product.price = request.data["price"]
        product.description = request.data['description']
        product.quantity = request.data['quantity ']
        product.city = request.data['city']
        product.created_at = request.data['created_at']
        product.image = request.data['image']
        product.product_type = request.data['product_type']
        product.customer = request.data['customer']
        product.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product are
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product= Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park areas resource
        Returns:
            Response -- JSON serialized list of park areas
        """
        product = Product.objects.all()  # This is my query to the database
        serializer = ProductSerializer(
            product, many=True, context={'request': request})
        return Response(serializer.data)
