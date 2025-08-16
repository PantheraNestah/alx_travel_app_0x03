from rest_framework import serializers
from .models import Listing, Booking

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        # Name each field you want to include in the API
        fields = ['id', 'title', 'description', 'price', 'owner']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        # Name each field for the booking endpoint
        fields = ['id', 'listing', 'guest', 'check_in_date', 'check_out_date']

# Serializer for payment initiation
class PaymentInitSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()

# Serializer for payment verification
class PaymentVerifySerializer(serializers.Serializer):
    transaction_id = serializers.CharField()