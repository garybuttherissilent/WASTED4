from django.contrib import admin
from .models import Route, Order, StreetAddress, RouteStreetAddress

admin.site.register(Route)
admin.site.register(Order)
admin.site.register(StreetAddress)
admin.site.register(RouteStreetAddress)
