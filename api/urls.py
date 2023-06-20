from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RouteViewSet, OrderViewSet, StreetAddressViewSet, RouteStreetAddressViewSet

router = DefaultRouter()
router.register(r'routes', RouteViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'streetaddresses', StreetAddressViewSet)
router.register(r'routestreetaddresses', RouteStreetAddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
