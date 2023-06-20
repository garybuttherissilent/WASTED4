# test_script.py
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wastedproject.settings')
django.setup()

from api.models import Complaint, Route, OrderQuerySet
from data_analysis import *

area = 'ZB'

# Mapping
area_routes_mapping = {
    'CA': ['T1', 'T2', 'T4', 'T5', 'C1', 'C2', 'C4', 'C5', 'C1A', 'C2A', 'C4A', 'C5A'],
    'ZA': ['T1', 'T2', 'T4', 'T5', 'Z1', 'Z2', 'Z4', 'Z5', 'Z1A', 'Z2A', 'Z4A', 'Z5A'],
    'CB': ['T1', 'T2', 'T4', 'T5', 'C1', 'C2', 'C4', 'C5', 'C1B', 'C2B', 'C4B', 'C5B'],
    'ZB': ['T1', 'T2', 'T4', 'T5', 'Z1', 'Z2', 'Z4', 'Z5', 'Z1B', 'Z2B', 'Z4B', 'Z5B']
}

routes = Route.objects.filter(day_of_week=2, area__in=area_routes_mapping[area])

df_list = []  # List to hold all dataframes
for route in routes:
    df = Complaint.objects.get_latest_complaints_by_route(route.route_id)
    if not df.empty:
        df_list.append((df, route.route_id))  # add to list if not empty







