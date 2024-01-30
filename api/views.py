from rest_framework import viewsets
from .models import Route, Order, StreetAddress, RouteStreetAddress
from .serializers import RouteSerializer, OrderSerializer, StreetAddressSerializer, RouteStreetAddressSerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class StreetAddressViewSet(viewsets.ModelViewSet):
    queryset = StreetAddress.objects.all()
    serializer_class = StreetAddressSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned street addresses to a given street name,
        by filtering against a `street_name` query parameter in the URL.
        """
        queryset = StreetAddress.objects.all()
        street_name = self.request.query_params.get('street_name', None)
        if street_name is not None:
            queryset = queryset.filter(street_name__istartswith=street_name)
        return queryset


# api.views

class RouteStreetAddressViewSet(viewsets.ModelViewSet):
    queryset = RouteStreetAddress.objects.all()
    serializer_class = RouteStreetAddressSerializer

    def get_queryset(self):
        queryset = RouteStreetAddress.objects.all()
        route_param = self.request.query_params.get('route', None)
        if route_param is not None:
            queryset = queryset.filter(route__route_id=route_param)
        return queryset
