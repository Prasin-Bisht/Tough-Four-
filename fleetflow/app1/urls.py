from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Vehicle URLs
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.vehicle_add, name='vehicle_add'),
    path('vehicles/edit/<int:pk>/', views.vehicle_edit, name='vehicle_edit'),
    path('vehicles/delete/<int:pk>/', views.vehicle_delete, name='vehicle_delete'),
    
    # Driver URLs
    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/add/', views.driver_add, name='driver_add'),
    path('drivers/edit/<int:pk>/', views.driver_edit, name='driver_edit'),
    path('drivers/delete/<int:pk>/', views.driver_delete, name='driver_delete'),
    
    # Trip URLs
    path('trips/', views.trip_list, name='trip_list'),
    path('trips/add/', views.trip_add, name='trip_add'),
    path('trips/edit/<int:pk>/', views.trip_edit, name='trip_edit'),
    path('trips/delete/<int:pk>/', views.trip_delete, name='trip_delete'),
    
    # Fuel Log URLs
    path('fuel/', views.fuel_list, name='fuel_list'),
    path('fuel/add/', views.fuel_add, name='fuel_add'),
    path('fuel/edit/<int:pk>/', views.fuel_edit, name='fuel_edit'),
    path('fuel/delete/<int:pk>/', views.fuel_delete, name='fuel_delete'),
    
    # Maintenance Log URLs
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/add/', views.maintenance_add, name='maintenance_add'),
    path('maintenance/edit/<int:pk>/', views.maintenance_edit, name='maintenance_edit'),
    path('maintenance/delete/<int:pk>/', views.maintenance_delete, name='maintenance_delete'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
]
