from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from base.models import (
    SportDetails, SportImage, Booking, Payment, TemporaryBookingData, SportReview, UserSportInteraction
)

# User model serializer
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'phone_number']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email is already in use.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Username already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name', ''),
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number']
        )
        return user

# Sport Image Serializer
class SportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportImage
        fields = ['image']

# Sport Review Serializer
class SportReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display user's email or username

    class Meta:
        model = SportReview
        fields = ['id', 'user', 'rating', 'review', 'created_at']

# Sport Details Serializer
class SportDetailsSerializer(serializers.ModelSerializer):
    sport_images = SportImageSerializer(many=True, read_only=True)
    reviews = SportReviewSerializer(many=True, read_only=True)

    class Meta:
        model = SportDetails
        fields = [
            'id', 'name', 'description', 'price', 'sport_images', 'sport_custom_id', 
            'category', 'location', 'created_at', 'average_rating','reviews']

# Booking Serializer
class BookingSerializer(serializers.ModelSerializer):
    sport_custom_id = serializers.CharField(source='sport.sport_custom_id', read_only=True)
    sport_category = serializers.CharField(source='sport.category', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'sport', 'sport_custom_id', 'sport_category', 'phone_number', 
            'date', 'start_time', 'end_time', 'amount', 'payment_status', 'booking_date'
        ]

# Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'booking', 'amount', 'payment_method', 'phone_number', 'transaction_uuid'
        ]

# Temporary Booking Data Serializer
class TemporaryBookingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryBookingData
        fields = [
            'id', 'booking_id', 'transaction_uuid', 'sport', 'user_id', 'phone_number', 
            'sport_custom_id', 'sport_category', 'date', 'start_time', 'end_time', 'amount'
        ]

# UserSportInteraction serializer
class UserSportInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSportInteraction
        fields = '__all__'