from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Vehicle, Booking
from .serializers import (
    UserRegistrationSerializer, 
    UserProfileSerializer,
    VehicleSerializer,
    BookingSerializer, 
    BookingCreateSerializer,
    BookingListSerializer
)


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'access': access_token,
                'refresh': refresh_token,
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'error': 'Registration failed',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'access': access_token,
                'refresh': refresh_token,
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class VehicleListCreateView(generics.ListCreateAPIView):
    """
    List user's vehicles and create new vehicles
    GET /vehicles/ - List user's vehicles
    POST /vehicles/ - Add a new vehicle
    """
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Vehicle.objects.filter(owner=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            vehicle = serializer.save()
            return Response({
                'message': 'Vehicle added successfully',
                'vehicle': VehicleSerializer(vehicle).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'error': 'Failed to add vehicle',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific vehicle
    GET /vehicles/{id}/ - Get vehicle details
    PUT /vehicles/{id}/ - Update vehicle
    DELETE /vehicles/{id}/ - Delete vehicle
    """
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Vehicle.objects.filter(owner=self.request.user)
    
    def get_object(self):
        queryset = self.get_queryset()
        vehicle_id = self.kwargs.get('pk')
        vehicle = get_object_or_404(queryset, id=vehicle_id)
        return vehicle
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        
        if serializer.is_valid():
            vehicle = serializer.save()
            return Response({
                'message': 'Vehicle updated successfully',
                'vehicle': VehicleSerializer(vehicle).data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'Failed to update vehicle',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if vehicle has active bookings
        active_bookings = Booking.objects.filter(
            vehicle=instance,
            status__in=['pending', 'confirmed']
        ).count()
        
        if active_bookings > 0:
            return Response({
                'error': 'Cannot delete vehicle with active bookings'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        instance.delete()
        return Response({
            'message': 'Vehicle deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class BookingListCreateView(generics.ListCreateAPIView):
    """
    List user's bookings and create new bookings
    GET /bookings/ - List user's bookings
    POST /bookings/ - Create a new booking
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookingCreateSerializer
        return BookingListSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            booking = serializer.save()
            response_serializer = BookingSerializer(booking)
            return Response({
                'message': 'Booking created successfully',
                'booking': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'error': 'Failed to create booking',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'bookings': serializer.data
        }, status=status.HTTP_200_OK)


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific booking
    GET /bookings/{id}/ - Get booking details
    PUT /bookings/{id}/ - Update booking
    DELETE /bookings/{id}/ - Cancel booking
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def get_object(self):
        queryset = self.get_queryset()
        booking_id = self.kwargs.get('pk')
        booking = get_object_or_404(queryset, id=booking_id)
        return booking
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Prevent updating completed or cancelled bookings
        if instance.status in ['completed', 'cancelled']:
            return Response({
                'error': f'Cannot update {instance.status} booking'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        
        if serializer.is_valid():
            booking = serializer.save()
            return Response({
                'message': 'Booking updated successfully',
                'booking': BookingSerializer(booking).data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'Failed to update booking',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Update status to cancelled instead of deleting
        if instance.status not in ['completed', 'cancelled']:
            instance.status = 'cancelled'
            instance.save()
            return Response({
                'message': 'Booking cancelled successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': f'Cannot cancel {instance.status} booking'
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics for the authenticated user
    """
    user = request.user
    
    vehicles_count = Vehicle.objects.filter(owner=user).count()
    bookings_count = Booking.objects.filter(user=user).count()
    active_bookings = Booking.objects.filter(
        user=user,
        status__in=['pending', 'confirmed']
    ).count()
    
    return Response({
        'stats': {
            'total_vehicles': vehicles_count,
            'total_bookings': bookings_count,
            'active_bookings': active_bookings,
        }
    }, status=status.HTTP_200_OK)
