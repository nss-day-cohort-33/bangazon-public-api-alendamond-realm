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
    Author: Curt Cato

    Arguments:
        serializers
    """

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'url', 'payment_type', 'customer_id', 'customer', 'created_at', 'line_items')
        depth = 2


class Orders(ViewSet):
    """Order items for Bangazon customers"""

    def create(self, request):
        """Handle POST operations

        Author: Curt Cato
        Purpose: Allow the user to create an order via communicating with the Bangazon DB
        Method: POST

        Returns:
            Response -- JSON serialized order instance
        """

        # Changing the orders resource by adding a product to an order means we have to make a new instance of OrderProduct. Let's do that first and add the product to it that was sent in the POST request:
        order_item = OrderProduct()
        order_item.product = Product.objects.get(pk=request.data["product_id"])

        # Now, we need to know whether order_item's order will be an existing order _or_ a new order we'll have to create:
        current_customer = Customer.objects.get(pk=request.user.id)
        order = Order.objects.filter(customer=current_customer, payment_type=None)

        # order is now either an existing, open order, or an empty queryset. How do we check? A new friend called exists()!
        if order.exists():
            print("Open order in db. Add it and the prod to OrderProduct")
            order_item.order = order[0]
        else:
            print("No open orders. Time to make a new order to add this product to")
            new_order = Order()
            new_order.customer = current_customer
            new_order.save()
            order_item.order = new_order

        # order_item has a product and an order. It's ready to save now
        order_item.save()

        # Convert the order to json and send it back to the client
        serializer = OrderSerializer(order_item, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single order

        Author: Curt Cato
        Purpose: Allow a user to communicate with the Bangazon database to retrieve one order
        Method:  GET

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

        Author: Curt Cato
        Purpose: Allow a user to update an order via the Bangazon DB
        Method: PUT

        Returns:
            Response -- Empty body with 204 status code
        """
        order = Order.objects.get(pk=pk)
        order.payment_type_id = PaymentType.objects.get(pk=request.data["payment_type_id"])
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a order are

        Author: Curt Cato
        Purpose: Allow a user to delete an order from the DB
        Method: DELETE

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

        Author: Curt Cato
        Purpose: Allow a user to list all of the order from the Bangazon DB

        Returns:
            Response -- JSON serialized list of orders
        """
        orders = Order.objects.all()
        customer = Customer.objects.get(pk=request.user.id)

        # Either send back all closed orders for the order history view, or the single open order to display in cart view
        cart = self.request.query_params.get('orderlist', None)
        orders = orders.filter(customer_id=customer)
        print("orders", orders)
        if cart is not None:
            orders = orders.filter(payment_type=None).get()
            print("orders filtered", orders)
            serializer = OrderSerializer(
                orders, many=False, context={'request': request}
              )
        else:
            serializer = OrderSerializer(
                orders, many=True, context={'request': request}
              )
        return Response(serializer.data)
