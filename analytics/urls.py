from django.urls import path, re_path
from .views import *

app_name = 'analytics'

# urls.py
urlpatterns = [
    path('dashboard_route/', dashboard_home_routes, name='dashboard_home_routes'),
    path('dashboard_route/view/', dashboard_view_routes, name='dashboard_view_routes'),
    path('dashboard_fraction/', dashboard_home_fractions, name='dashboard_home_fractions'),
    path('dashboard_fraction/view/', dashboard_view_fractions, name='dashboard_view_fractions')

]

