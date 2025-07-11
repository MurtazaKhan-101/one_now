from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from .models import Vehicle, Booking


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'username', 'date_joined')


class VehicleSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Vehicle
        fields = ('id', 'owner', 'make', 'model', 'year', 'plate', 'created_at', 'updated_at')
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')

    def validate_year(self, value):
        current_year = timezone.now().year
        if value < 1900 or value > current_year + 1:
            raise serializers.ValidationError(f'Year must be between 1900 and {current_year + 1}')
        return value

    def validate_plate(self, value):
        value = value.upper().strip()
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            existing_vehicle = Vehicle.objects.filter(plate=value).exclude(
                id=self.instance.id if self.instance else None
            ).first()
            
            if existing_vehicle:
                raise serializers.ValidationError('A vehicle with this license plate already exists')
        
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        return super().create(validated_data)


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)
    duration_days = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = (
            'id', 'user', 'vehicle', 'vehicle_details', 'start_date', 'end_date', 
            'status', 'duration_days', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'duration_days')

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        vehicle = attrs.get('vehicle')

        # Validate date range
        if start_date >= end_date:
            raise serializers.ValidationError("End date must be after start date")
        
        if start_date < timezone.now():
            raise serializers.ValidationError("Start date cannot be in the past")

        # Check for overlapping bookings for the same vehicle
        if vehicle:
            overlapping_bookings = Booking.objects.filter(
                vehicle=vehicle,
                status__in=['pending', 'confirmed'],
                start_date__lt=end_date,
                end_date__gt=start_date
            )
            
            # Exclude current booking if updating
            if self.instance:
                overlapping_bookings = overlapping_bookings.exclude(id=self.instance.id)
            
            if overlapping_bookings.exists():
                raise serializers.ValidationError(
                    "Vehicle is already booked for the selected time period"
                )

        return attrs

    def validate_vehicle(self, value):
        request = self.context.get('request')
        if not Vehicle.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Selected vehicle does not exist")
        
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class BookingCreateSerializer(BookingSerializer):
    class Meta(BookingSerializer.Meta):
        fields = ('vehicle', 'start_date', 'end_date')


class BookingListSerializer(serializers.ModelSerializer):
    vehicle_info = serializers.SerializerMethodField()
    duration_days = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = (
            'id', 'vehicle_info', 'start_date', 'end_date', 
            'status', 'duration_days', 'created_at'
        )

    def get_vehicle_info(self, obj):
        return f"{obj.vehicle.year} {obj.vehicle.make} {obj.vehicle.model} ({obj.vehicle.plate})"
