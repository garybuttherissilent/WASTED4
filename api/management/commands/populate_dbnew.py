from django.core.management import BaseCommand
from api.models import Route, Order, StreetAddress, RouteStreetAddress
import numpy as np
import pandas as pd
from data_preparation.data_preparation import addresses_df, orders_df
import uuid
from django.db.utils import IntegrityError

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        route_attributes_mapping = {}

        for _, row in orders_df.iterrows():
            day_of_week = row['day_of_week']
            calendar = row['calendar']

            try:
                route, created = Route.objects.get_or_create(
                    route_id=row['Route'],
                    fraction=row['Fractie'],
                    city_or_rural=row['city_or_rural'],
                    area=row['Gebied'],  # Adding 'Gebied' value as 'area'
                    day_of_week=day_of_week,  # Adding 'day_of_week' value
                    calendar=calendar,
                )
                if created:
                    print(f"New Route created: {route}")
            except IntegrityError:
                route = Route.objects.get(route_id=row['Route'])

            if created:
                route_attributes_mapping[row['Route']] = {'fraction': row['Fractie'], 'city_or_rural': row['city_or_rural'], 'area': row['Gebied'], 'day_of_week': day_of_week, 'calendar': calendar}

            Order.objects.create(
                order_id=uuid.uuid4(),
                route=route,
                date=row['Orderdatum'],
                vehicle=row['Voertuig'],
                weight=row['Gewicht afval']
            )

        # Populate the StreetAddress model
        for _, row in addresses_df.iterrows():
            lat = row['Latitude']
            lon = row['Longitude']

            lat = float(lat) if not pd.isna(lat) else None
            lon = float(lon) if not pd.isna(lon) else None

            street_address, created = StreetAddress.objects.get_or_create(
                street_name=row['Straatnaam'],
                even_range=row['Even_Range'],
                odd_range=row['Odd_Range'],
                defaults={
                    'zip_code': row['Postcode'],
                    'purpose': row['Bestemming'],
                    'area': row['Gebied']
                },
            )
            if created:
                print(f"New StreetAddress created: {street_address}")

            route_ids = [row[i] for i in ['Rest', 'PMD', 'Papier', 'Glas', 'GFT_Zomer'] if pd.notna(row[i])]
            for route_id in route_ids:
                route_attributes = route_attributes_mapping.get(route_id, {'fraction': 'unknown', 'city_or_rural': 'unknown', 'area': 'unknown', 'calendar': 'unknown','day_of_week': 8})
                try:
                    route, created = Route.objects.get_or_create(route_id=route_id, **route_attributes)
                    if created:
                        print(f"New Route created: {route}")
                except IntegrityError:
                    route = Route.objects.get(route_id=route_id)

                RouteStreetAddress.objects.get_or_create(route=route, street_address=street_address)
