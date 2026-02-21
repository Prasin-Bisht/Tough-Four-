from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import Vehicle, Driver, Trip, FuelLog, MaintenanceLog
from .forms import (
    UserRegisterForm, VehicleForm, DriverForm, 
    TripForm, FuelLogForm, MaintenanceLogForm
)


# ============================================================
# AUTHENTICATION VIEWS
# ============================================================

def user_login(request):
    """
    User login view.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def register(request):
    """
    User registration view.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to FleetFlow.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})


def user_logout(request):
    """
    User logout view.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ============================================================
# DASHBOARD VIEW
# ============================================================

@login_required
def dashboard(request):
    """
    Dashboard view showing summary statistics.
    """
    # Get counts for summary cards
    active_vehicles = Vehicle.objects.filter(status='active').count()
    active_drivers = Driver.objects.filter(is_available=True).count()
    
    # Maintenance due (within next 7 days or overdue)
    today = timezone.now().date()
    maintenance_due = MaintenanceLog.objects.filter(
        next_due_date__lte=today + timedelta(days=7),
        next_due_date__gte=today
    ).count()
    
    # Additional stats
    total_vehicles = Vehicle.objects.count()
    total_drivers = Driver.objects.count()
    total_trips = Trip.objects.count()
    completed_trips = Trip.objects.filter(status='completed').count()
    total_fuel_cost = FuelLog.objects.aggregate(Sum('cost'))['cost__sum'] or 0
    total_maintenance_cost = MaintenanceLog.objects.aggregate(Sum('cost'))['cost__sum'] or 0
    
    # Recent activities
    recent_trips = Trip.objects.select_related('vehicle', 'driver').order_by('-created_at')[:5]
    recent_fuel_logs = FuelLog.objects.select_related('vehicle').order_by('-date')[:5]
    
    context = {
        'active_vehicles': active_vehicles,
        'active_drivers': active_drivers,
        'maintenance_due': maintenance_due,
        'total_vehicles': total_vehicles,
        'total_drivers': total_drivers,
        'total_trips': total_trips,
        'completed_trips': completed_trips,
        'total_fuel_cost': total_fuel_cost,
        'total_maintenance_cost': total_maintenance_cost,
        'recent_trips': recent_trips,
        'recent_fuel_logs': recent_fuel_logs,
    }
    
    return render(request, 'dashboard.html', context)


# ============================================================
# VEHICLE VIEWS
# ============================================================

@login_required
def vehicle_list(request):
    """
    List all vehicles.
    """
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicles/list.html', {'vehicles': vehicles})


@login_required
def vehicle_add(request):
    """
    Add a new vehicle.
    """
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle added successfully!")
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    
    return render(request, 'vehicles/form.html', {'form': form, 'action': 'Add'})


@login_required
def vehicle_edit(request, pk):
    """
    Edit an existing vehicle.
    """
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle updated successfully!")
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    
    return render(request, 'vehicles/form.html', {'form': form, 'action': 'Edit', 'vehicle': vehicle})


@login_required
def vehicle_delete(request, pk):
    """
    Delete a vehicle.
    """
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, "Vehicle deleted successfully!")
        return redirect('vehicle_list')
    
    return render(request, 'vehicles/delete.html', {'vehicle': vehicle})


# ============================================================
# DRIVER VIEWS
# ============================================================

@login_required
def driver_list(request):
    """
    List all drivers.
    """
    drivers = Driver.objects.select_related('assigned_vehicle').all()
    return render(request, 'drivers/list.html', {'drivers': drivers})


@login_required
def driver_add(request):
    """
    Add a new driver.
    """
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Driver added successfully!")
            return redirect('driver_list')
    else:
        form = DriverForm()
    
    return render(request, 'drivers/form.html', {'form': form, 'action': 'Add'})


@login_required
def driver_edit(request, pk):
    """
    Edit an existing driver.
    """
    driver = get_object_or_404(Driver, pk=pk)
    
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, "Driver updated successfully!")
            return redirect('driver_list')
    else:
        form = DriverForm(instance=driver)
    
    return render(request, 'drivers/form.html', {'form': form, 'action': 'Edit', 'driver': driver})


@login_required
def driver_delete(request, pk):
    """
    Delete a driver.
    """
    driver = get_object_or_404(Driver, pk=pk)
    
    if request.method == 'POST':
        driver.delete()
        messages.success(request, "Driver deleted successfully!")
        return redirect('driver_list')
    
    return render(request, 'drivers/delete.html', {'driver': driver})


# ============================================================
# TRIP VIEWS
# ============================================================

@login_required
def trip_list(request):
    """
    List all trips.
    """
    trips = Trip.objects.select_related('vehicle', 'driver').all()
    return render(request, 'trips/list.html', {'trips': trips})


@login_required
def trip_add(request):
    """
    Add a new trip.
    """
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Trip created successfully!")
            return redirect('trip_list')
    else:
        form = TripForm()
    
    return render(request, 'trips/form.html', {'form': form, 'action': 'Create'})


@login_required
def trip_edit(request, pk):
    """
    Edit an existing trip.
    """
    trip = get_object_or_404(Trip, pk=pk)
    
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, "Trip updated successfully!")
            return redirect('trip_list')
    else:
        form = TripForm(instance=trip)
    
    return render(request, 'trips/form.html', {'form': form, 'action': 'Edit', 'trip': trip})


@login_required
def trip_delete(request, pk):
    """
    Delete a trip.
    """
    trip = get_object_or_404(Trip, pk=pk)
    
    if request.method == 'POST':
        trip.delete()
        messages.success(request, "Trip deleted successfully!")
        return redirect('trip_list')
    
    return render(request, 'trips/delete.html', {'trip': trip})


# ============================================================
# FUEL LOG VIEWS
# ============================================================

@login_required
def fuel_list(request):
    """
    List all fuel logs.
    """
    fuel_logs = FuelLog.objects.select_related('vehicle').all()
    total_cost = fuel_logs.aggregate(Sum('cost'))['cost__sum'] or 0
    total_quantity = fuel_logs.aggregate(Sum('fuel_quantity'))['fuel_quantity__sum'] or 0
    
    context = {
        'fuel_logs': fuel_logs,
        'total_cost': total_cost,
        'total_quantity': total_quantity,
    }
    return render(request, 'fuel/list.html', context)


@login_required
def fuel_add(request):
    """
    Add a new fuel log.
    """
    if request.method == 'POST':
        form = FuelLogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fuel log added successfully!")
            return redirect('fuel_list')
    else:
        form = FuelLogForm()
    
    return render(request, 'fuel/form.html', {'form': form, 'action': 'Add'})


@login_required
def fuel_edit(request, pk):
    """
    Edit an existing fuel log.
    """
    fuel_log = get_object_or_404(FuelLog, pk=pk)
    
    if request.method == 'POST':
        form = FuelLogForm(request.POST, instance=fuel_log)
        if form.is_valid():
            form.save()
            messages.success(request, "Fuel log updated successfully!")
            return redirect('fuel_list')
    else:
        form = FuelLogForm(instance=fuel_log)
    
    return render(request, 'fuel/form.html', {'form': form, 'action': 'Edit', 'fuel_log': fuel_log})


@login_required
def fuel_delete(request, pk):
    """
    Delete a fuel log.
    """
    fuel_log = get_object_or_404(FuelLog, pk=pk)
    
    if request.method == 'POST':
        fuel_log.delete()
        messages.success(request, "Fuel log deleted successfully!")
        return redirect('fuel_list')
    
    return render(request, 'fuel/delete.html', {'fuel_log': fuel_log})


# ============================================================
# MAINTENANCE LOG VIEWS
# ============================================================

@login_required
def maintenance_list(request):
    """
    List all maintenance logs.
    """
    maintenance_logs = MaintenanceLog.objects.select_related('vehicle').all()
    total_cost = maintenance_logs.aggregate(Sum('cost'))['cost__sum'] or 0
    
    # Get upcoming maintenance
    today = timezone.now().date()
    upcoming = maintenance_logs.filter(next_due_date__gte=today).order_by('next_due_date')[:5]
    
    context = {
        'maintenance_logs': maintenance_logs,
        'total_cost': total_cost,
        'upcoming': upcoming,
    }
    return render(request, 'maintenance/list.html', context)


@login_required
def maintenance_add(request):
    """
    Add a new maintenance log.
    """
    if request.method == 'POST':
        form = MaintenanceLogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Maintenance log added successfully!")
            return redirect('maintenance_list')
    else:
        form = MaintenanceLogForm()
    
    return render(request, 'maintenance/form.html', {'form': form, 'action': 'Add'})


@login_required
def maintenance_edit(request, pk):
    """
    Edit an existing maintenance log.
    """
    maintenance_log = get_object_or_404(MaintenanceLog, pk=pk)
    
    if request.method == 'POST':
        form = MaintenanceLogForm(request.POST, instance=maintenance_log)
        if form.is_valid():
            form.save()
            messages.success(request, "Maintenance log updated successfully!")
            return redirect('maintenance_list')
    else:
        form = MaintenanceLogForm(instance=maintenance_log)
    
    return render(request, 'maintenance/form.html', {'form': form, 'action': 'Edit', 'maintenance_log': maintenance_log})


@login_required
def maintenance_delete(request, pk):
    """
    Delete a maintenance log.
    """
    maintenance_log = get_object_or_404(MaintenanceLog, pk=pk)
    
    if request.method == 'POST':
        maintenance_log.delete()
        messages.success(request, "Maintenance log deleted successfully!")
        return redirect('maintenance_list')
    
    return render(request, 'maintenance/delete.html', {'maintenance_log': maintenance_log})


# ============================================================
# REPORTS VIEW
# ============================================================

@login_required
def reports(request):
    """
    Reports view showing analytics and statistics.
    """
    # Vehicle statistics
    vehicle_stats = {
        'total': Vehicle.objects.count(),
        'active': Vehicle.objects.filter(status='active').count(),
        'inactive': Vehicle.objects.filter(status='inactive').count(),
        'maintenance': Vehicle.objects.filter(status='maintenance').count(),
    }
    
    # Driver statistics
    driver_stats = {
        'total': Driver.objects.count(),
        'available': Driver.objects.filter(is_available=True).count(),
        'assigned': Driver.objects.filter(is_available=False).count(),
    }
    
    # Trip statistics
    trip_stats = {
        'total': Trip.objects.count(),
        'pending': Trip.objects.filter(status='pending').count(),
        'in_progress': Trip.objects.filter(status='in_progress').count(),
        'completed': Trip.objects.filter(status='completed').count(),
        'cancelled': Trip.objects.filter(status='cancelled').count(),
        'total_distance': Trip.objects.aggregate(Sum('distance'))['distance__sum'] or 0,
    }
    
    # Fuel statistics
    fuel_stats = {
        'total_entries': FuelLog.objects.count(),
        'total_cost': FuelLog.objects.aggregate(Sum('cost'))['cost__sum'] or 0,
        'total_quantity': FuelLog.objects.aggregate(Sum('fuel_quantity'))['fuel_quantity__sum'] or 0,
    }
    
    # Maintenance statistics
    maintenance_stats = {
        'total_entries': MaintenanceLog.objects.count(),
        'total_cost': MaintenanceLog.objects.aggregate(Sum('cost'))['cost__sum'] or 0,
    }
    
    # Monthly fuel costs (last 6 months)
    from django.db.models.functions import TruncMonth
    monthly_fuel = FuelLog.objects.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total_cost=Sum('cost'),
        total_quantity=Sum('fuel_quantity')
    ).order_by('-month')[:6]
    
    # Recent vehicles
    recent_vehicles = Vehicle.objects.order_by('-created_at')[:5]
    
    # Recent trips
    recent_trips = Trip.objects.select_related('vehicle', 'driver').order_by('-created_at')[:5]
    
    context = {
        'vehicle_stats': vehicle_stats,
        'driver_stats': driver_stats,
        'trip_stats': trip_stats,
        'fuel_stats': fuel_stats,
        'maintenance_stats': maintenance_stats,
        'monthly_fuel': monthly_fuel,
        'recent_vehicles': recent_vehicles,
        'recent_trips': recent_trips,
    }
    
    return render(request, 'reports.html', context)
