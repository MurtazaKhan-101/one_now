from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta
from .models import Vehicle, Booking


class AuthenticationTestCase(TestCase):
    """Test cases for user authentication"""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('backend:register')
        self.login_url = reverse('backend:login')
        
    def test_user_registration_success(self):
        """Test successful user registration"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('user', response.data)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        
    def test_user_registration_password_mismatch(self):
        """Test registration with password mismatch"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'differentpass',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_user_login_success(self):
        """Test successful user login"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {'username': 'wronguser', 'password': 'wrongpass'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_user_login_missing_fields(self):
        """Test login with missing required fields"""
        data = {'username': 'testuser'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class VehicleModelTestCase(TestCase):
    """Test cases for Vehicle model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
    def test_vehicle_creation(self):
        """Test creating a new vehicle"""
        vehicle = Vehicle.objects.create(
            owner=self.user,
            make='Toyota',
            model='Corolla',
            year=2020,
            plate='ABC-123'
        )
        self.assertEqual(str(vehicle), '2020 Toyota Corolla (ABC-123)')
        self.assertEqual(vehicle.owner, self.user)
        
    def test_vehicle_unique_plate(self):
        """Test that license plates are unique"""
        Vehicle.objects.create(
            owner=self.user,
            make='Toyota',
            model='Corolla',
            year=2020,
            plate='ABC-123'
        )
        
        user2 = User.objects.create_user(username='testuser2', password='testpass123')
        with self.assertRaises(Exception):
            Vehicle.objects.create(
                owner=user2,
                make='Honda',
                model='Civic',
                year=2021,
                plate='ABC-123'
            )


class VehicleAPITestCase(TestCase):
    """Test cases for Vehicle API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
        self.vehicle_list_url = reverse('backend:vehicle_list_create')
        
    def test_create_vehicle_success(self):
        """Test successful vehicle creation"""
        data = {
            'make': 'Toyota',
            'model': 'Corolla',
            'year': 2020,
            'plate': 'ABC-123'
        }
        response = self.client.post(self.vehicle_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Vehicle.objects.filter(plate='ABC-123').exists())
        
    def test_create_vehicle_invalid_year(self):
        """Test vehicle creation with invalid year"""
        data = {
            'make': 'Toyota',
            'model': 'Corolla',
            'year': 1800,  # Invalid year
            'plate': 'ABC-123'
        }
        response = self.client.post(self.vehicle_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_list_user_vehicles(self):
        """Test listing user's vehicles"""
        Vehicle.objects.create(
            owner=self.user,
            make='Toyota',
            model='Corolla',
            year=2020,
            plate='ABC-123'
        )
        response = self.client.get(self.vehicle_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_update_vehicle(self):
        """Test updating a vehicle"""
        vehicle = Vehicle.objects.create(
            owner=self.user,
            make='Toyota',
            model='Corolla',
            year=2020,
            plate='ABC-123'
        )
        url = reverse('backend:vehicle_detail', kwargs={'pk': vehicle.id})
        data = {'make': 'Honda', 'model': 'Civic', 'year': 2021, 'plate': 'XYZ-789'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.make, 'Honda')
        
    def test_delete_vehicle(self):
        """Test deleting a vehicle"""
        vehicle = Vehicle.objects.create(
            owner=self.user,
            make='Toyota',
            model='Corolla',
            year=2020,
            plate='ABC-123'
        )
        url = reverse('backend:vehicle_detail', kwargs={'pk': vehicle.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vehicle.objects.filter(id=vehicle.id).exists())


class BookingModelTestCase(TestCase):
    """Test cases for Booking model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.vehicle = Vehicle.objects.create(
            owner=self.user,
            make='Toyota',
            model='Corolla',
            year=2020,
            plate='ABC-123'
        )
        
    def test_booking_creation(self):
        """Test creating a new booking"""
        start_date = timezone.now() + timedelta(days=1)
        end_date = start_date + timedelta(days=3)
        
        booking = Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=start_date,
            end_date=end_date
        )
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.vehicle, self.vehicle)
        self.assertEqual(booking.duration_days, 3)
        
    def test_booking_str_representation(self):
        """Test booking string representation"""
        start_date = timezone.now() + timedelta(days=1)
        end_date = start_date + timedelta(days=3)
        
        booking = Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=start_date,
            end_date=end_date
        )
        expected_str = f"Booking {booking.id} - {self.vehicle} ({start_date} to {end_date})"
        self.assertEqual(str(booking), expected_str)


class BookingAPITestCase(TestCase):
    """Test cases for Booking API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
        self.vehicle = Vehicle.objects.create(
            owner=self.user,
            make='Toyota',
            model='Corolla',
            year=2020,
            plate='ABC-123'
        )
        
        self.booking_list_url = reverse('backend:booking_list_create')
        
    def test_create_booking_success(self):
        """Test successful booking creation"""
        start_date = timezone.now() + timedelta(days=1)
        end_date = start_date + timedelta(days=3)
        
        data = {
            'vehicle': self.vehicle.id,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
        response = self.client.post(self.booking_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Booking.objects.filter(vehicle=self.vehicle).exists())
        
    def test_create_booking_invalid_dates(self):
        """Test booking creation with invalid dates"""
        start_date = timezone.now() + timedelta(days=3)
        end_date = timezone.now() + timedelta(days=1)  # End before start
        
        data = {
            'vehicle': self.vehicle.id,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
        response = self.client.post(self.booking_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_booking_past_date(self):
        """Test booking creation with past start date"""
        start_date = timezone.now() - timedelta(days=1)  # Past date
        end_date = timezone.now() + timedelta(days=1)
        
        data = {
            'vehicle': self.vehicle.id,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
        response = self.client.post(self.booking_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_list_user_bookings(self):
        """Test listing user's bookings"""
        start_date = timezone.now() + timedelta(days=1)
        end_date = start_date + timedelta(days=3)
        
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=start_date,
            end_date=end_date
        )
        
        response = self.client.get(self.booking_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        
    def test_overlapping_bookings(self):
        """Test prevention of overlapping bookings"""
        start_date = timezone.now() + timedelta(days=1)
        end_date = start_date + timedelta(days=3)
        
        # Create first booking
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=start_date,
            end_date=end_date
        )
        
        # Try to create overlapping booking
        overlap_start = start_date + timedelta(days=1)
        overlap_end = end_date + timedelta(days=1)
        
        data = {
            'vehicle': self.vehicle.id,
            'start_date': overlap_start.isoformat(),
            'end_date': overlap_end.isoformat()
        }
        response = self.client.post(self.booking_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DashboardStatsTestCase(TestCase):
    """Test cases for dashboard statistics"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
        self.stats_url = reverse('backend:dashboard_stats')
        
    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        # Create test data
        vehicle = Vehicle.objects.create(
            owner=self.user,
            make='Toyota',
            model='Corolla',
            year=2020,
            plate='ABC-123'
        )
        
        start_date = timezone.now() + timedelta(days=1)
        end_date = start_date + timedelta(days=3)
        
        Booking.objects.create(
            user=self.user,
            vehicle=vehicle,
            start_date=start_date,
            end_date=end_date,
            status='pending'
        )
        
        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        stats = response.data['stats']
        self.assertEqual(stats['total_vehicles'], 1)
        self.assertEqual(stats['total_bookings'], 1)
        self.assertEqual(stats['active_bookings'], 1)