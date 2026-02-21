from django.db import models
from django.contrib.auth.models import User


# ============================================================
# VEHICLE MODEL
# ============================================================
class Vehicle(models.Model):
    """
    Vehicle model to store fleet vehicle information.
    """
    # Vehicle type choices
    VEHICLE_TYPES = [
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('car', 'Car'),
        ('bus', 'Bus'),
        ('motorcycle', 'Motorcycle'),
    ]
    
    # Status choices
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
    ]
    
    vehicle_number = models.CharField(max_length=50, unique=True, help_text="Unique vehicle identifier")
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES, default='truck')
    capacity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Capacity in tons or liters")
    purchase_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Vehicles"
    
    def __str__(self):
        return f"{self.vehicle_number} - {self.get_vehicle_type_display()}"
    
    @property
    def is_active(self):
        return self.status == 'active'


# ============================================================
# DRIVER MODEL
# ============================================================
class Driver(models.Model):
    """
    Driver model to store driver information.
    """
    driver_name = models.CharField(max_length=200, help_text="Full name of the driver")
    phone = models.CharField(max_length=20, help_text="Phone number")
    license_number = models.CharField(max_length=50, unique=True, help_text="Driver's license number")
    experience = models.IntegerField(help_text="Years of driving experience")
    assigned_vehicle = models.OneToOneField(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='driver')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Drivers"
    
    def __str__(self):
        return self.driver_name


# ============================================================
# TRIP MODEL
# ============================================================
class Trip(models.Model):
    """
    Trip model to track vehicle trips.
    """
    # Trip status choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='trips')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='trips')
    start_location = models.CharField(max_length=200)
    end_location = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2, help_text="Distance in km")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Trips"
    
    def __str__(self):
        return f"Trip #{self.id} - {self.start_location} to {self.end_location}"


# ============================================================
# FUEL LOG MODEL
# ============================================================
class FuelLog(models.Model):
    """
    Fuel log model to track fuel consumption.
    """
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fuel_logs')
    date = models.DateField()
    fuel_quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Fuel quantity in liters")
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total cost")
    odometer_reading = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Odometer reading in km")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name_plural = "Fuel Logs"
    
    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.date} - ${self.cost}"


# ============================================================
# MAINTENANCE LOG MODEL
# ============================================================
class MaintenanceLog(models.Model):
    """
    Maintenance log model to track vehicle maintenance.
    """
    # Maintenance type choices
    MAINTENANCE_TYPES = [
        ('oil_change', 'Oil Change'),
        ('tire_rotation', 'Tire Rotation'),
        ('brake_service', 'Brake Service'),
        ('engine_service', 'Engine Service'),
        ('general_checkup', 'General Checkup'),
        ('other', 'Other'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_logs')
    maintenance_type = models.CharField(max_length=50, choices=MAINTENANCE_TYPES)
    date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    next_due_date = models.DateField(null=True, blank=True, help_text="Next maintenance due date")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name_plural = "Maintenance Logs"
    
    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.get_maintenance_type_display()} - {self.date}"
    
    @property
    def is_due(self):
        from django.utils import timezone
        if self.next_due_date:
            return self.next_due_date <= timezone.now().date()
        return False
