from rest_framework import serializers
from .models import Route, Order, StreetAddress, RouteStreetAddress

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['route_id', 'fraction', 'area', 'city_or_rural', 'day_of_week']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'route', 'date', 'vehicle', 'weight']

class StreetAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreetAddress
        fields = ['address_id', 'street_name', 'zip_code', 'purpose', 'area', 'latitude', 'longitude']

class RouteStreetAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteStreetAddress
        fields = ['route', 'street_address']
