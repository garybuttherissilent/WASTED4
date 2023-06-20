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

            try:
                route, created = Route.objects.get_or_create(
                    route_id=row['Route'],
                    fraction=row['Fractie'],
                    city_or_rural=row['city_or_rural'],
                    area=row['Gebied'],  # Adding 'Gebied' value as 'area'
                    day_of_week=day_of_week,  # Adding 'day_of_week' value
                )
                if created:
                    print(f"New Route created: {route}")
            except IntegrityError:
                route = Route.objects.get(route_id=row['Route'])

            if created:
                route_attributes_mapping[row['Route']] = {'fraction': row['Fractie'], 'city_or_rural': row['city_or_rural'], 'area': row['Gebied'], 'day_of_week': day_of_week}

            Order.objects.create(
                order_id=uuid.uuid4(),
                route=route,
                date=row['Orderdatum'],
                vehicle=row['Voertuig'],
                weight=row['Gewicht afval']
            )

        for _, row in addresses_df.iterrows():
            lat, lon = (np.nan, np.nan) if pd.isna(row['Coordinates']) else row['Coordinates'].split(',')

            lat = lat.strip() if lat is not np.nan else lat
            lon = lon.strip() if lon is not np.nan else lon

            lat = float(lat) if lat not in {'None', np.nan} else None
            lon = float(lon) if lon not in {'None', np.nan} else None

            street_address, created = StreetAddress.objects.get_or_create(
                street_name=row['Straatnaam'],
                zip_code=row['Postcode'],
                area=row['Gebied'],
                purpose=row['Bestemming'],
                latitude=lat,
                longitude=lon,
            )
            if created:
                print(f"New StreetAddress created: {street_address}")

            route_ids = [row[i] for i in ['Rest', 'PMD', 'Papier', 'Glas', 'GFT_Zomer'] if pd.notna(row[i])]
            for route_id in route_ids:
                route_attributes = route_attributes_mapping.get(route_id, {'fraction': 'unknown', 'city_or_rural': 'unknown', 'area': 'unknown', 'day_of_week': 8})
                try:
                    route, created = Route.objects.get_or_create(route_id=route_id, **route_attributes)
                    if created:
                        print(f"New Route created: {route}")
                except IntegrityError:
                    route = Route.objects.get(route_id=route_id)

                RouteStreetAddress.objects.get_or_create(route=route, street_address=street_address)
