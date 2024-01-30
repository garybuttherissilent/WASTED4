from django.shortcuts import render
from api.models import StreetAddress, RouteStreetAddress
import folium
from geopy.geocoders import Nominatim

def search_street(request):
    if request.method == 'GET':
        street_name = request.GET.get('q', '')
        house_number = request.GET.get('house_number', '').strip()

        is_odd = None
        house_number_provided = bool(house_number)
        if house_number_provided:
            try:
                house_number = int(house_number)
                is_odd = house_number % 2 == 1
            except ValueError:
                house_number_provided = False

        coordinates = []
        geolocator = Nominatim(user_agent="WASTED")

        routes_dict = {
            'REST': set(),
            'PMD': set(),
            'GFT': set(),
            'GLAS': set(),
            'PAPIER': set()
        }

        def add_routes(address):
            in_odd_range = False
            in_even_range = False
            # Check for 'nan-nan' in odd and even ranges
            odd_range_nan = address.odd_range == 'nan-nan'
            even_range_nan = address.even_range == 'nan-nan'
            both_ranges_nan_nan = address.odd_range == 'nan-nan' and address.even_range == 'nan-nan'

            if house_number_provided and not both_ranges_nan_nan:
                if address.odd_range and 'nan' not in address.odd_range:
                    odd_range_start, odd_range_end = map(float, address.odd_range.split('-'))
                    in_odd_range = is_odd and odd_range_start <= house_number <= odd_range_end

                if address.even_range and 'nan' not in address.even_range:
                    even_range_start, even_range_end = map(float, address.even_range.split('-'))
                    in_even_range = not is_odd and even_range_start <= house_number <= even_range_end

                # Check odd range if it is not 'nan-nan' and the house number is odd
                if not odd_range_nan and is_odd:
                    odd_range_start, odd_range_end = address.odd_range.split('-')
                    in_odd_range = float(odd_range_start) <= house_number <= float(odd_range_end)

                # Check even range if it is not 'nan-nan' and the house number is even
                if not even_range_nan and not is_odd:
                    even_range_start, even_range_end = address.even_range.split('-')
                    in_even_range = float(even_range_start) <= house_number <= float(even_range_end)

                if not in_odd_range and not in_even_range:
                    return  # Skip if house number is not in the range

            routes_street_addresses = RouteStreetAddress.objects.filter(street_address=address)
            for rsa in routes_street_addresses:
                route_id = rsa.route.route_id
                if 'HHRES' in route_id:
                    routes_dict['REST'].add(route_id)
                elif 'HHPMD' in route_id:
                    routes_dict['PMD'].add(route_id)
                elif 'HHGF' in route_id:
                    routes_dict['GFT'].add(route_id)
                elif 'HHPAP' in route_id:
                    routes_dict['PAPIER'].add(route_id)
                elif 'HHGLS' in route_id:
                    routes_dict['GLAS'].add(route_id)

        def geocode_address(full_address):
            location = geolocator.geocode(full_address)
            if location:
                coordinates.append((location.latitude, location.longitude))
                return True
            return False

        if street_name:
            addresses = StreetAddress.objects.filter(street_name=street_name)
            for address in addresses:
                full_address = f"{street_name} {house_number}, {address.zip_code}" if house_number_provided else f"{street_name}, {address.zip_code}"

                if not geocode_address(full_address):
                    # Fallback to geocode without house number if both ranges are 'nan-nan'
                    if address.odd_range == 'nan-nan' and address.even_range == 'nan-nan':
                        geocode_address(f"{street_name}, {address.zip_code}")
                    continue

                add_routes(address)

        map_html = None
        if coordinates:
            street_map = folium.Map(location=coordinates[0], zoom_start=13, control_scale=True)
            for coord in coordinates:
                folium.Marker(coord).add_to(street_map)
            map_html = street_map._repr_html_()

        if not street_name or not any(routes_dict.values()):
            routes_dict = None
            map_html = None
        else:
            for key, value in routes_dict.items():
                routes_dict[key] = list(value)

        return render(request, 'streetseeker2/search_street.html', {'routes_dict': routes_dict, 'map': map_html})
    else:
        return render(request, 'streetseeker2/search_street.html')