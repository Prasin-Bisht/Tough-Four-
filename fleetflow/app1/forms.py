from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Vehicle, Driver, Trip, FuelLog, MaintenanceLog


# ============================================================
# USER REGISTRATION FORM
# ============================================================
class UserRegisterForm(UserCreationForm):
    """
    Form for user registration.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # Add CSS classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['email', 'first_name', 'last_name']:
                field.widget.attrs['class'] = 'form-control'
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Username'
    
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


# ============================================================
# VEHICLE FORM
# ============================================================
class VehicleForm(forms.ModelForm):
    """
    Form for creating and updating vehicles.
    """
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'vehicle_type', 'capacity', 'purchase_date', 'status']
        widgets = {
            'vehicle_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter vehicle number'
            }),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter capacity',
                'step': '0.01'
            }),
            'purchase_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


# ============================================================
# DRIVER FORM
# ============================================================
class DriverForm(forms.ModelForm):
    """
    Form for creating and updating drivers.
    """
    class Meta:
        model = Driver
        fields = ['driver_name', 'phone', 'license_number', 'experience', 'assigned_vehicle', 'is_available']
        widgets = {
            'driver_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter driver name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'license_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter license number'
            }),
            'experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Years of experience'
            }),
            'assigned_vehicle': forms.Select(attrs={'class': 'form-select'}),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


# ============================================================
# TRIP FORM
# ============================================================
class TripForm(forms.ModelForm):
    """
    Form for creating and updating trips.
    """
    class Meta:
        model = Trip
        fields = ['vehicle', 'driver', 'start_location', 'end_location', 'distance', 'status', 'notes']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'driver': forms.Select(attrs={'class': 'form-select'}),
            'start_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter start location'
            }),
            'end_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter end location'
            }),
            'distance': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Distance in km',
                'step': '0.01'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Additional notes',
                'rows': 3
            }),
        }


# ============================================================
# FUEL LOG FORM
# ============================================================
class FuelLogForm(forms.ModelForm):
    """
    Form for creating and updating fuel logs.
    """
    class Meta:
        model = FuelLog
        fields = ['vehicle', 'date', 'fuel_quantity', 'cost', 'odometer_reading']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fuel_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fuel quantity in liters',
                'step': '0.01'
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Total cost',
                'step': '0.01'
            }),
            'odometer_reading': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Odometer reading in km',
                'step': '0.01'
            }),
        }


# ============================================================
# MAINTENANCE LOG FORM
# ============================================================
class MaintenanceLogForm(forms.ModelForm):
    """
    Form for creating and updating maintenance logs.
    """
    class Meta:
        model = MaintenanceLog
        fields = ['vehicle', 'maintenance_type', 'date', 'cost', 'description', 'next_due_date']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'maintenance_type': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cost',
                'step': '0.01'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description',
                'rows': 3
            }),
            'next_due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
