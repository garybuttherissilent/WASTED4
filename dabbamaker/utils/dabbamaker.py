import requests
import pandas as pd
import folium
from folium import DivIcon
import re



def get_addresses(excel_file):
    # Read the Excel file
    df = pd.read_excel(excel_file)
    df = df[pd.notna(df['Uitvoerdersinfo'])]
    addresses = []
    for i, row in df.iterrows():
        # Extract the address using regular expressions
        match = re.search(r'HH COMF_(.*?)_', row['Uitvoerdersinfo'])
        if match:
            addresses.append(match.group(1))
    df = pd.DataFrame(addresses, columns=['address'])
    return df

def sort_by_zipcode_order(address_df):
    zip_codes = {'9051': 1, '9031': 2, '9030': 3, '9000': 4, '9032': 5, '9042': 6, '9041': 7, '9040': 8, '9050': 9, '9052' : 10}
    address_df['zip_code'] = address_df['address'].str.extract(r'(?<!\S{4})(9[0-9]{3})\s[A-Z]{1}[A-Za-z]{1,}')
    address_df['zip_code_num'] = address_df['zip_code'].map(zip_codes)
    address_df = address_df.sort_values(by=['zip_code_num','address'])
    address_list = address_df.values.tolist()
    return address_list


def simple_address_list(address_list):
    streets = []
    for address in address_list:
        match = re.search(r'^(\D+)\s(\d+)', address[0])
        if match:
            street_name = match.group(1)
            street_number = match.group(2)
            street = street_name + ' ' + street_number
            streets.append(street)
    return streets


def get_coordinates(address):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={address}, Ghent, Belgium&format=json"
        response = requests.get(url)
        data = response.json()
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        coord = [lat, lon]
        return coord
    except:
        return None


def dabba_coord_list_maker(address_list):
    address_list_coords = []
    for street_name in address_list:
        street_coords = get_coordinates(street_name)
        if street_coords:
            address_list_coords.append(street_coords)
    return address_list_coords


def mapmaker(address_list_coords):
    # Create a map of Ghent centered at the coordinates (51.05, 3.7167)
    ghent_map = folium.Map(location=[51.05, 3.7167], zoom_start=13, control_scale=True)
    # add markers with numbers
    for i, coord in enumerate(address_list_coords):
        # add number marker
        folium.Marker(location=coord, icon=DivIcon(icon_size=(30, 36), icon_anchor=(-20, 18),
                                                   html=f'<div style="font-size: 12pt; font-weight: bold;">{i + 1}</div>')).add_to(
            ghent_map)

        # add location marker
        folium.Marker(location=coord).add_to(ghent_map)
    return ghent_map

def create_legend(suburb_dict, address_list):
    legend_html = '<div id="legend-container" style="width: 20%; height: 100%; position: fixed; top: 2px; left: 5px; z-index:9999; font-size: 14pt; overflow-y: scroll; background-color:white;">'
    counter = 1
    for i, suburb in enumerate(suburb_dict.keys()):
        legend_html += f'<b>{suburb}</b><br>'
        for address in suburb_dict[suburb]:
            legend_html += f'{counter}. {address}<br>' # Add the marker number before the address
            counter += 1
    legend_html += '</div>'
    return legend_html


def get_suburb(address):
    match = re.search(r'\b([A-Za-z-]+)$', address[0]) # Extract the last word of the string
    if match:
        return match.group(1)
    else:
        return None

def save_map_with_legend(excel_file):
    address_list = sort_by_zipcode_order(get_addresses(excel_file))
    suburbs = {}
    for address in address_list:
        suburb = get_suburb(address)
        if suburb:
            if suburb not in suburbs:
                suburbs[suburb] = []
            match = re.search(r'^[^\d]*\d+', address[0])
            simplified_address = match.group()
            suburbs[suburb].append(simplified_address)

    ghent_map = mapmaker(dabba_coord_list_maker(simple_address_list(address_list)))
    legend_html = create_legend(suburbs, address_list)
    ghent_map._parent.get_root().html.add_child(folium.Element(legend_html))

    # Render the map to HTML and return as a string
    return ghent_map._parent.get_root().render()








