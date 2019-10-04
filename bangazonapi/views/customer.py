# """View module for handling requests about customers"""
# from django.http import HttpResponseServerError
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import serializers
# from rest_framework import status
# from kennywoodapi.models import Customer


# class CustomerSerializer(serializers.HyperlinkedModelSerializer):
#     """JSON serializer for park areas
#     Arguments:
#         serializers
#     """
#     class Meta:
#         model = Customer
#         url = serializers.HyperlinkedIdentityField(
#             view_name='attraction',
#             lookup_field='id'
#         )
#         fields = ('id', 'address', 'phone_number', 'user')


# class Customers(ViewSet):
#     """Park Areas for Kennywood Amusement Park"""

#     def create(self, request):
#         """Handle POST operations
#         Returns:
#             Response -- JSON serialized Attraction instance
#         """
#         new_attraction = Customers()
#         new_attraction.name = request.data["first_name"]

#         area = ParkArea.objects.get(pk=request.data["area_id"])
#         new_attraction.area = area
#         new_attraction.save()

#         serializer = AttractionSerializer(new_attraction, context={'request': request})

#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         """Handle GET requests for single park area
#         Returns:
#             Response -- JSON serialized park area instance
#         """
#         try:
#             area = Attraction.objects.get(pk=pk)
#             serializer = AttractionSerializer(area, context={'request': request})
#             return Response(serializer.data)
#         except Exception as ex:
#             return HttpResponseServerError(ex)

#     def update(self, request, pk=None):
#         """Handle PUT requests for a park area attraction
#         Returns:
#             Response -- Empty body with 204 status code
#         """
#         attraction = Attraction.objects.get(pk=pk)
#         area = ParkArea.objects.get(pk=request.data["area_id"])
#         attraction.name = request.data["name"]
#         attraction.area = area
#         attraction.save()

#         return Response({}, status=status.HTTP_204_NO_CONTENT)

#     def destroy(self, request, pk=None):
#         """Handle DELETE requests for a single park are
#         Returns:
#             Response -- 200, 404, or 500 status code
#         """
#         try:
#             area = Attraction.objects.get(pk=pk)
#             area.delete()

#             return Response({}, status=status.HTTP_204_NO_CONTENT)

#         except Attraction.DoesNotExist as ex:
#             return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

#         except Exception as ex:
#             return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def list(self, request):
#         """Handle GET requests to park attractions resource
#         Returns:
#             Response -- JSON serialized list of park attractions
#         """
#         attractions = Attraction.objects.all()

#         # Support filtering attractions by area id
#         area = self.request.query_params.get('area', None)
#         if area is not None:
#             attractions = attractions.filter(area__id=area)

#         serializer = AttractionSerializer(
#             attractions, many=True, context={'request': request})
#         return Response(serializer.data)