"""View module for handling requests about customers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from bangazonapi.models import Customer



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'user_id', 'email', 'first_name', 'last_name', 'date_joined', 'is_active')


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas
    Arguments:
        serializers
    """
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'url', 'address', 'phone_number', 'user_id')
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


        user = User.objects.get(pk=request.data["user_id"])
        user = User.objects.get(first_name=request.data["first_name"])
        user = User.objects.get(last_name=request.data["last_name"])
        user = User.objects.get(is_active=request.data["is_active"])
        user = User.objects.get(username=request.data["username"])
        user = User.objects.get(email=request.data["email"])
        user = User.objects.get(date_joined=request.data["date_joined"])
        new_customer.user = user
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
        """Handle GET requests to itinerary resource
        Returns:
            Response -- JSON serialized list of customer itineraries
        """
        customer = Customer.objects.get(user=request.auth.user)
        # customer = Customer.objects.all()
        serializer = CustomerSerializer(
           customer, many=True, context={'request': request})
        return Response(serializer.data)



# class UserSerializer(serializers.HyperlinkedModelSerializer):
#       class Meta:
#         model = User
#         fields = ('id', 'url', 'user_id', 'email', 'first_name', 'last_name', 'date_joined', 'is_active')

# class CustomerSerializer(serializers.HyperlinkedModelSerializer):
#     """JSON serializer for customers
#     Arguments:
#         serializers.HyperlinkedModelSerializer
#     """
#     class Meta:
#         model = Customer
#         url = serializers.HyperlinkedIdentityField(
#             view_name='customer',
#         )
#         fields = ('id', 'url', 'user_id', 'address', 'phone_number')
#         depth = 1




    # def retrieve(self, request, pk=None):
    #     """Handle GET requests for single park area
    #     Returns:
    #         Response -- JSON serialized park area instance
    #     """
    #     try:
    #         area = Attraction.objects.get(pk=pk)
    #         serializer = AttractionSerializer(area, context={'request': request})
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    # def update(self, request, pk=None):
    #     """Handle PUT requests for a park area attraction
    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     attraction = Attraction.objects.get(pk=pk)
    #     area = ParkArea.objects.get(pk=request.data["area_id"])
    #     attraction.name = request.data["name"]
    #     attraction.area = area
    #     attraction.save()

    #     return Response({}, status=status.HTTP_204_NO_CONTENT)

    # def destroy(self, request, pk=None):
    #     """Handle DELETE requests for a single park are
    #     Returns:
    #         Response -- 200, 404, or 500 status code
    #     """
    #     try:
    #         area = Attraction.objects.get(pk=pk)
    #         area.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except Attraction.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    """View module for handling requests about customers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from bangazonapi.models import Customer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'user_id', 'email')
class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customers
    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
        )
        fields = ('id', 'url', 'user_id', 'address', 'phone_number')
        depth = 1
class Customers(ViewSet):
    """Customers for Bangazon Galaydia Empire"""
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Customer instance
        """
        newcustomer = Customer()
        newcustomer.address = request.data["address"]
        newcustomer.phone_number = request.data["phone_number"]
        newcustomer.save()
        serializer = CustomerSerializer(newcustomer, context={'request': request})
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

