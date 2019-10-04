# """View module for handling requests about park areas"""
# from django.http import HttpResponseServerError
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import serializers
# from rest_framework import status
# from bangazonapi.models import ProductType


# class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
#     """JSON serializer for product types

#     Arguments:
#         serializers
#     """
#     class Meta:
#         model = ProductType
#         url = serializers.HyperlinkedIdentityField(
#             view_name='producttype',
#             lookup_field='id'
#         )
#         fields = ('id', 'url', 'name')
#         depth = 2


# class ProductTypes(ViewSet):
#     """Product types for Bangazon"""

#     def create(self, request):
#         """Handle POST operations

#         Returns:
#             Response -- JSON serialized Attraction instance
#         """
#         new_itinerary_item = Itinerary()
#         new_itinerary_item.attraction = Attraction.objects.get(pk=request.data["attraction_id"])
#         new_itinerary_item.customer = Customer.objects.get(user=request.auth.user)
#         new_itinerary_item.starttime = request.data["starttime"]

#         new_itinerary_item.save()

#         serializer = ItineraryItemSerializer(new_itinerary_item, context={'request': request})

#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         """Handle GET requests for single park area

#         Returns:
#             Response -- JSON serialized park area instance
#         """
#         try:
#             itinerary_item = Itinerary.objects.get(pk=pk)
#             serializer = ItineraryItemSerializer(itinerary_item, context={'request': request})
#             return Response(serializer.data)
#         except Exception as ex:
#             return HttpResponseServerError(ex)

#     def update(self, request, pk=None):
#         """Handle PUT requests for a park area attraction

#         Returns:
#             Response -- Empty body with 204 status code
#         """
#         itinerary_item = Itinerary.objects.get(pk=pk)
#         itinerary_item.starttime = request.data["starttime"]
#         itinerary_item.save()

#         return Response({}, status=status.HTTP_204_NO_CONTENT)

#     def destroy(self, request, pk=None):
#         """Handle DELETE requests for a single park are

#         Returns:
#             Response -- 200, 404, or 500 status code
#         """
#         try:
#             itinerary_item = Itinerary.objects.get(pk=pk)
#             itinerary_item.delete()

#             return Response({}, status=status.HTTP_204_NO_CONTENT)

#         except Attraction.DoesNotExist as ex:
#             return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

#         except Exception as ex:
#             return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def list(self, request):
#         """Handle GET requests to list itinerary items for authenicated customer

#         Returns:
#             Response -- JSON serialized list of park attractions
#         """
#         customer = Customer.objects.get(user=request.auth.user)
#         items = Itinerary.objects.filter(customer=customer)

#         serializer = ItineraryItemSerializer(
#             items, many=True, context={'request': request})
#         return Response(serializer.data)
