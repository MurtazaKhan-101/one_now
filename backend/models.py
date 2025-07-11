from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone


class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=50, help_text="Vehicle manufacturer (e.g., Toyota, Honda)")
    model = models.CharField(max_length=50, help_text="Vehicle model (e.g., Corolla, Civic)")
    year = models.PositiveIntegerField(help_text="Manufacturing year")
    plate = models.CharField(
        max_length=20, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z0-9\s\-]+$',
                message='License plate must contain only letters, numbers, spaces, and hyphens'
            )
        ],
        help_text="Vehicle license plate number"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'plate']

    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.plate})"

    def clean(self):
        from django.core.exceptions import ValidationError
        current_year = timezone.now().year
        if self.year < 1900 or self.year > current_year + 1:
            raise ValidationError(f'Year must be between 1900 and {current_year + 1}')


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateTimeField(help_text="Booking start date and time")
    end_date = models.DateTimeField(help_text="Booking end date and time")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking {self.id} - {self.vehicle} ({self.start_date} to {self.end_date})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_date >= self.end_date:
            raise ValidationError('End date must be after start date')
        
        if self.start_date < timezone.now():
            raise ValidationError('Start date cannot be in the past')

    @property
    def duration_days(self):
        """Calculate booking duration in days"""
        return (self.end_date - self.start_date).days