import django
import os
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wastedproject.settings')
django.setup()

from api.models import Route, Order

route_id = 'HHRESZ401'

# Retrieve the route object with the route ID 'HHRESK401'
route = Route.objects.get(route_id=route_id)

# Get the queryset for orders with the given route ID
orders = Order.objects.filter(route=route)

# Print out the details of each order in the queryset
for order in orders:
    print(f"Order ID: {order.order_id}")
    print(f"Date: {order.date}")
    print(f"Vehicle: {order.vehicle}")
    print(f"Weight: {order.weight}")
    print()
