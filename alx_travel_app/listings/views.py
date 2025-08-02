from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Listing objects.
    
    Provides CRUD operations for listings including:
    - list: Get all listings
    - create: Create a new listing
    - retrieve: Get a specific listing
    - update: Update a listing
    - partial_update: Partially update a listing
    - destroy: Delete a listing
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    
    @swagger_auto_schema(
        operation_description="Get all listings",
        responses={
            200: ListingSerializer(many=True),
            400: "Bad Request"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Create a new listing",
        request_body=ListingSerializer,
        responses={
            201: ListingSerializer,
            400: "Bad Request"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Get a specific listing by ID",
        responses={
            200: ListingSerializer,
            404: "Not Found"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Update a listing",
        request_body=ListingSerializer,
        responses={
            200: ListingSerializer,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Partially update a listing",
        request_body=ListingSerializer,
        responses={
            200: ListingSerializer,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Delete a listing",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Booking objects.
    
    Provides CRUD operations for bookings including:
    - list: Get all bookings
    - create: Create a new booking
    - retrieve: Get a specific booking
    - update: Update a booking
    - partial_update: Partially update a booking
    - destroy: Delete a booking
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    @swagger_auto_schema(
        operation_description="Get all bookings",
        responses={
            200: BookingSerializer(many=True),
            400: "Bad Request"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Create a new booking",
        request_body=BookingSerializer,
        responses={
            201: BookingSerializer,
            400: "Bad Request"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Get a specific booking by ID",
        responses={
            200: BookingSerializer,
            404: "Not Found"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Update a booking",
        request_body=BookingSerializer,
        responses={
            200: BookingSerializer,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Partially update a booking",
        request_body=BookingSerializer,
        responses={
            200: BookingSerializer,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Delete a booking",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
