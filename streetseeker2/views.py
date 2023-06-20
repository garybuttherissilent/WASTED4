from django.shortcuts import render
from api.models import StreetAddress, RouteStreetAddress
import folium
import logging

logger = logging.getLogger(__name__)

def search_street(request):
    logger.info(
        'my_view was called - path: %s, method: %s, status: %s',
        request.path,
        request.method
    )
    if request.method == 'GET':
        street_name = request.GET.get('q', '')  # if nothing is provided, default to an empty string

        # Initialize a dictionary to hold the routes
        routes_dict = {
            'REST': [],
            'PMD': [],
            'GFT': [],
            'GLAS': [],
            'PAPIER': []

        }

        if street_name:
            try:
                # Find the street addresses that match the input street name
                addresses = StreetAddress.objects.filter(street_name=street_name)

                # For each address, find the associated routes and add them to the dictionary
                for address in addresses:
                    routes_street_addresses = RouteStreetAddress.objects.filter(street_address=address)

                    for rsa in routes_street_addresses:
                        route_id = rsa.route.route_id

                        if 'HHRES' in route_id:
                            routes_dict['REST'].append(route_id)
                        elif 'HHPMD' in route_id:
                            routes_dict['PMD'].append(route_id)
                        elif 'HHGF' in route_id:
                            routes_dict['GFT'].append(route_id)
                        elif 'HHPAP' in route_id:
                            routes_dict['PAPIER'].append(route_id)
                        elif 'HHGLS' in route_id:
                            routes_dict['GLAS'].append(route_id)
            except StreetAddress.DoesNotExist:
                pass

        coordinates = []

        if routes_dict:
            # Find the street addresses with coordinates
            addresses_with_coords = StreetAddress.objects.filter(street_name=street_name, latitude__isnull=False, longitude__isnull=False)

            # If any addresses with coordinates are found, add the coordinates to the list
            for address in addresses_with_coords:
                coordinates.append((address.latitude, address.longitude))

        map_html = None
        if coordinates:
            # If the coordinates list is not empty, use the first coordinate for map center
            street_map = folium.Map(location=[coordinates[0][0], coordinates[0][1]], zoom_start=13, control_scale=True)
            # Add a marker to the map for each set of coordinates
            for coord in coordinates:
                folium.Marker(coord).add_to(street_map)
            # Render the map to an HTML string
            map_html = street_map._repr_html_()

        if not street_name or not routes_dict:
            # If no street name is provided or no routes are found, set routes_dict and map_html to None
            routes_dict = None
            map_html = None

        return render(request, 'streetseeker2/search_street.html', {'routes_dict': routes_dict, 'map': map_html})
    else:
        return render(request, 'streetseeker2/search_street.html')
