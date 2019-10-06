"""View module for handling requests about payment types"""
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import *


class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Payment Types

    Author: Joy Ittycheriah
    methods: none

    Arguments:
        serializers
    """

    customer = serializers.HyperlinkedRelatedField(
        queryset=Customer.objects.all(),
        view_name="customer-detail",
        many=True,
        required=False,
        lookup_field="pk"
    )

    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymenttype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'merchant_name', 'acct_number',
                  'created_at', 'expiration_date', 'customer')
        depth = 1


class PaymentTypes(ViewSet):
    """Payment Types for Bangazon"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Payment Type instance
        """
        new_payment_type = PaymentType()
        new_payment_type.merchant_name = request.data["merchant_name"]
        new_payment_type.acct_number = request.data["acct_number"]
        new_payment_type.expiration_date = request.data["expiration_date"]

        customer = Customer.objects.get(pk=request.data["customer"])
        new_payment_type.customer = customer
        new_payment_type.save()

        serializer = PaymentTypeSerializer(
            new_payment_type, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single payment type

        Returns:
            Response -- JSON serialized payment type instance
        """
        try:
            payment_type = PaymentType.objects.get(pk=pk)
            serializer = PaymentTypeSerializer(
                payment_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a single payment type

        Returns:
            Response -- Empty body with 204 status code
        """
        update_payment_type = PaymentType.objects.get(pk=pk)

        customer = Customer.objects.get(pk=request.data["customer"])

        update_payment_type.merchant_name = request.data["merchant_name"]
        update_payment_type.acct_number = request.data["acct_number"]
        update_payment_type.expiration_date = request.data["expiration_date"]

        update_payment_type.customer = customer
        update_payment_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single payment type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            this_payment_type = PaymentType.objects.get(pk=pk)
            this_payment_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to payment types resource

        Returns:
            Response -- JSON serialized list of payment types
        """
        payment_types = PaymentType.objects.all()

        # Support filtering payment types by customer
        this_customer = self.request.query_params.get('customer', None)
        if this_customer is not None:
            payment_types = payment_types.filter(customer=this_customer)

        serializer = PaymentTypeSerializer(
            payment_types, many=True, context={'request': request})
        return Response(serializer.data)
