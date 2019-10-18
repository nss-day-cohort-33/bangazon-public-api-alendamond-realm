"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bangazonapi.models import ProductType, Product
from bangazonapi.views.product import ProductSerializer

class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for product types

    Arguments:
        serializers
    """
    products = ProductSerializer(many=True)

    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='producttype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'products', 'total_products')
        depth = 2


class ProductTypes(ViewSet):
    """Product types for Bangazon"""

    permission_classes = (IsAuthenticatedOrReadOnly,)
    def create(self, request):

        """Handle POST operations

        Returns:
            Response -- JSON serialized ProductType instance
        """

        new_product_type = ProductType()
        new_product_type.name = request.data["name"]
        new_product_type.save()

        serializer = ProductTypeSerializer(new_product_type, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product type

        Returns:
            Response -- JSON serialized ProductType instance
        """
        try:
            product_type = ProductType.objects.get(pk=pk)
            serializer = ProductTypeSerializer(product_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a product type

        Returns:
            Response -- Empty body with 204 status code
        """
        product_type = ProductType.objects.get(pk=pk)
        product_type.name = request.data["name"]
        product_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product_type = ProductType.objects.get(pk=pk)
            product_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProductType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to product types resource

        Returns:
            Response -- JSON serialized list of product types
        """
        types = ProductType.objects.all()

        includeproducts = self.request.query_params.get('includeproducts', None)

        if includeproducts is not None:
            for product_type in types:
                related_products = Product.objects.filter(product_type=product_type)[:3]
                product_type.products = related_products

        serializer = ProductTypeSerializer(
            types, many=True, context={'request': request})
        return Response(serializer.data)



