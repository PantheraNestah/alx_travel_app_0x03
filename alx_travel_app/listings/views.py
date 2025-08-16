from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated
import requests
from django.conf import settings
from .serializers import ListingSerializer, BookingSerializer, PaymentInitSerializer
from .serializers import PaymentVerifySerializer
from rest_framework import serializers
from rest_framework.decorators import action



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
        operation_description="Create a new booking and initiate payment",
        request_body=BookingSerializer,
        responses={
            201: openapi.Response(
                "Booking created and payment initiated",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'booking': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'payment': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'checkout_url': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Bad Request"
        }
    )
    def create(self, request, *args, **kwargs):
        # Create the booking
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        # Initiate payment for the booking
        CHAPA_SECRET = getattr(settings, "CHAPA_SECRET", None)
        if not CHAPA_SECRET:
            return Response({"detail": "Chapa secret key not configured."}, status=500)

        chapa_url = "https://api.chapa.co/v1/transaction/initialize"
        amount = float(booking.listing.price)
        user = booking.guest
        payload = {
            "amount": amount,
            "currency": "ETB",
            "email": user.email or "test@example.com",
            "first_name": user.first_name or "User",
            "last_name": user.last_name or "",
            "tx_ref": f"booking_{booking.id}_{user.id}",
            "return_url": "http://localhost:8000/api/payment/verify/",  # Update as needed
            "customization[title]": "Travel Booking Payment",
            "customization[description]": f"Payment for booking {booking.id}",
        }
        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET}",
            "Content-Type": "application/json",
        }
        try:
            chapa_resp = requests.post(chapa_url, json=payload, headers=headers, timeout=10)
            chapa_data = chapa_resp.json()
            if chapa_resp.status_code != 200 or chapa_data.get("status") != "success":
                return Response({"detail": "Failed to initiate payment with Chapa.", "chapa_response": chapa_data}, status=502)
            checkout_url = chapa_data["data"]["checkout_url"]
            transaction_id = chapa_data["data"]["tx_ref"]
        except Exception as e:
            return Response({"detail": f"Error contacting Chapa: {str(e)}"}, status=502)

        # Store payment record
        payment = Payment.objects.create(
            booking=booking,
            amount=amount,
            status="pending",
            transaction_id=transaction_id,
        )

        # Prepare response
        booking_data = BookingSerializer(booking).data
        payment_data = {
            "id": payment.id,
            "status": payment.status,
            "transaction_id": payment.transaction_id,
            "amount": str(payment.amount),
        }
        return Response({
            "booking": booking_data,
            "payment": payment_data,
            "checkout_url": checkout_url,
        }, status=201)
    
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


# PaymentViewSet for payment-related actions
class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method="post",
        request_body=PaymentInitSerializer,
        responses={200: openapi.Response("Payment initiated", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'checkout_url': openapi.Schema(type=openapi.TYPE_STRING),
                'transaction_id': openapi.Schema(type=openapi.TYPE_STRING),
                'status': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ))}
    )
    @action(detail=False, methods=["post"], url_path="initiate", url_name="initiate")
    def initiate_payment(self, request):
        """
        Initiate payment for a booking using Chapa API.
        """
        serializer = PaymentInitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking_id = serializer.validated_data["booking_id"]
        try:
            booking = Booking.objects.get(id=booking_id, guest=request.user)
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=404)

        # Check if payment already exists
        if hasattr(booking, "payment"):
            return Response({"detail": "Payment already initiated for this booking."}, status=400)

        # Chapa API integration
        CHAPA_SECRET = getattr(settings, "CHAPA_SECRET", None)
        if not CHAPA_SECRET:
            return Response({"detail": "Chapa secret key not configured."}, status=500)

        chapa_url = "https://api.chapa.co/v1/transaction/initialize"
        amount = float(booking.listing.price)
        payload = {
            "amount": amount,
            "currency": "ETB",
            "email": request.user.email or "test@example.com",
            "first_name": request.user.first_name or "User",
            "last_name": request.user.last_name or "",
            "tx_ref": f"booking_{booking.id}_{request.user.id}",
            "return_url": "http://localhost:8000/api/payment/verify/",  # Update as needed
            "customization[title]": "Travel Booking Payment",
            "customization[description]": f"Payment for booking {booking.id}",
        }
        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET}",
            "Content-Type": "application/json",
        }
        try:
            chapa_resp = requests.post(chapa_url, json=payload, headers=headers, timeout=10)
            chapa_data = chapa_resp.json()
            if chapa_resp.status_code != 200 or chapa_data.get("status") != "success":
                return Response({"detail": "Failed to initiate payment with Chapa.", "chapa_response": chapa_data}, status=502)
            checkout_url = chapa_data["data"]["checkout_url"]
            transaction_id = chapa_data["data"]["tx_ref"]
        except Exception as e:
            return Response({"detail": f"Error contacting Chapa: {str(e)}"}, status=502)

        # Store payment record
        payment = Payment.objects.create(
            booking=booking,
            amount=amount,
            status="pending",
            transaction_id=transaction_id,
        )

        return Response({
            "checkout_url": checkout_url,
            "transaction_id": transaction_id,
            "status": payment.status,
        })
    
    @swagger_auto_schema(
        method="post",
        request_body=PaymentVerifySerializer,
        responses={200: openapi.Response("Payment verification", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'transaction_id': openapi.Schema(type=openapi.TYPE_STRING),
                'status': openapi.Schema(type=openapi.TYPE_STRING),
                'detail': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ))}
    )
    @action(detail=False, methods=["post"], url_path="verify", url_name="verify")
    def verify_payment(self, request):
        """
        Verify payment status with Chapa and update Payment model.
        """
        serializer = PaymentVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction_id = serializer.validated_data["transaction_id"]

        # Find the payment record
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment record not found.", "transaction_id": transaction_id}, status=404)

        CHAPA_SECRET = getattr(settings, "CHAPA_SECRET", None)
        if not CHAPA_SECRET:
            return Response({"detail": "Chapa secret key not configured."}, status=500)

        chapa_url = f"https://api.chapa.co/v1/transaction/verify/{transaction_id}"
        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET}",
            "Content-Type": "application/json",
        }
        try:
            chapa_resp = requests.get(chapa_url, headers=headers, timeout=10)
            chapa_data = chapa_resp.json()
            if chapa_resp.status_code != 200 or chapa_data.get("status") != "success":
                payment.status = "failed"
                payment.save()
                return Response({
                    "transaction_id": transaction_id,
                    "status": payment.status,
                    "detail": "Payment verification failed.",
                    "chapa_response": chapa_data
                }, status=502)
            # Chapa returns payment status in chapa_data["data"]["status"]
            chapa_status = chapa_data["data"].get("status", "")
            if chapa_status == "success":
                payment.status = "completed"
            else:
                payment.status = "failed"
            payment.save()
        except Exception as e:
            payment.status = "failed"
            payment.save()
            return Response({
                "transaction_id": transaction_id,
                "status": payment.status,
                "detail": f"Error contacting Chapa: {str(e)}"
            }, status=502)

        return Response({
            "transaction_id": transaction_id,
            "status": payment.status,
            "detail": "Payment verification complete."
        })
