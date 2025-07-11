from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'backend'

urlpatterns = [
    # Authentication endpoints
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    
    # Vehicle management endpoints
    path('vehicles/', views.VehicleListCreateView.as_view(), name='vehicle_list_create'),
    path('vehicles/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    
    # Booking management endpoints
    path('bookings/', views.BookingListCreateView.as_view(), name='booking_list_create'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    
    # Dashboard stats
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
]
