from django.contrib import admin

from .models import User, Vehicle, Booking

admin.site.register(Vehicle)
admin.site.register(Booking)
