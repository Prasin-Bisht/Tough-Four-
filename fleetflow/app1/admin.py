from django.contrib import admin
from .models import Vehicle, Driver, Trip, FuelLog, MaintenanceLog


# ============================================================
# Admin configuration for Vehicle model
# ============================================================
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_number', 'vehicle_type', 'capacity', 'status', 'created_at']
    list_filter = ['vehicle_type', 'status']
    search_fields = ['vehicle_number']
    ordering = ['-created_at']


# ============================================================
# Admin configuration for Driver model
# ============================================================
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['driver_name', 'phone', 'license_number', 'experience', 'is_available', 'created_at']
    list_filter = ['is_available', 'experience']
    search_fields = ['driver_name', 'license_number']
    ordering = ['-created_at']


# ============================================================
# Admin configuration for Trip model
# ============================================================
@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle', 'driver', 'start_location', 'end_location', 'distance', 'status', 'created_at']
    list_filter = ['status', 'vehicle__vehicle_type']
    search_fields = ['start_location', 'end_location', 'vehicle__vehicle_number', 'driver__driver_name']
    ordering = ['-created_at']
    raw_id_fields = ['vehicle', 'driver']


# ============================================================
# Admin configuration for FuelLog model
# ============================================================
@admin.register(FuelLog)
class FuelLogAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'date', 'fuel_quantity', 'cost', 'created_at']
    list_filter = ['date', 'vehicle__vehicle_type']
    search_fields = ['vehicle__vehicle_number']
    ordering = ['-date', '-created_at']
    raw_id_fields = ['vehicle']


# ============================================================
# Admin configuration for MaintenanceLog model
# ============================================================
@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'maintenance_type', 'date', 'cost', 'next_due_date', 'created_at']
    list_filter = ['maintenance_type', 'date', 'vehicle__vehicle_type']
    search_fields = ['vehicle__vehicle_number', 'description']
    ordering = ['-date', '-created_at']
    raw_id_fields = ['vehicle']
