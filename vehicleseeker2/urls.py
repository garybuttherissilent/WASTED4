from django.urls import path
from . import views

app_name = 'vehicleseeker2'

urlpatterns = [
    path('search_vehicle/', views.vehicle_search_view, name='search_vehicle'),
]
