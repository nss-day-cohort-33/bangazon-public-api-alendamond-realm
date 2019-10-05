"""View module for handling requests about payment types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import PaymentType


class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Payment Type

    Author: Joy Ittycheriah
    methods: none

    Arguments:
        serializers
    """
    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymenttype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'merchant_name',
                  'acct_number', 'created_at', 'expiration_date', 'customer')


class ListPaymentTypes(ViewSet):
    """Payment Types for Bangazon"""

    # def create(self, request):
    #     """Handle POST operations

    #     Returns:
    #         Response -- JSON serialized ParkArea instance
    #     """
    #     new_payment_type = PaymentType()
    #     new_payment_type.merchant_name = request.data["merchant_name"]
    #     new_payment_type.acct_number = request.data["acct_number"]
    #     new_payment_type.save()

    #     serializer = PaymentTypeSerializer(new_payment_type, context={'request': request})

    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     """Handle GET requests for single payment type

    #     Returns:
    #         Response -- JSON serialized payment type instance
    #     """
    #     try:
    #         new_payment_type = PaymentType.objects.get(pk=pk)
    #         serializer = PaymentTypeSerializer(
    #             area, context={'request': request})
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    # def update(self, request, pk=None):
    #     """Handle PUT requests for a park area

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     area = ParkArea.objects.get(pk=pk)
    #     area.name = request.data["name"]
    #     area.theme = request.data["theme"]
    #     area.save()

    #     return Response({}, status=status.HTTP_204_NO_CONTENT)

    # def destroy(self, request, pk=None):
    #     """Handle DELETE requests for a single park area

    #     Returns:
    #         Response -- 200, 404, or 500 status code
    #     """
    #     try:
    #         area = ParkArea.objects.get(pk=pk)
    #         area.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except ParkArea.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to payment types resource

        Returns:
            Response -- JSON serialized list of payment types
        """
        paymenttype = PaymentType.objects.all()
        serializer = PaymentTypeSerializer(
            paymenttype, many=True, context={'request': request})
        return Response(serializer.data)
