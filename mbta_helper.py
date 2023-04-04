# Your API KEYS (you need to use your own keys - very long random characters)
# from config import MAPBOX_TOKEN, MBTA_API_KEY
import requests
import json
import math
from math import radians, cos, sin, asin, sqrt
# Useful URLs (you need to add the appropriate parameters for your requests)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


# A little bit of scaffolding if you want to use it

def distance(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate distance
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    return distance


def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.
    Both get_lat_long() and get_nearest_station() might need to use this function.
    """
    response = requests.get(url)
    data = response.json()
    return data
    pass


def get_lat_long(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{place_name}.json?access_token=pk.eyJ1IjoiYWRyaWFuY3Jpb2xsbyIsImEiOiJjbGZ2dGFwNXMwMTA2M2RxN3YwdGN4amNpIn0.QVp_50lEd72_KTRGfz-PPA"   
    data = get_json(url)
    coords = data['features'][0]['geometry']['coordinates']
    lat_long = (coords[1],coords[0])
    return lat_long
    
def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    response = requests.get(f'https://api-v3.mbta.com/stops?sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}')
    data = response.json()
    mapdict = data["data"][0]
    station_name = mapdict['attributes']['name']
    if(mapdict['attributes']['wheelchair_boarding'] >= 1):
        wheelchair = True
    else:
        wheelchair = False

    return (station_name,wheelchair)



def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
    long_lat = get_lat_long(place_name)
    nearest_station = get_nearest_station(long_lat[0],long_lat[1])
    return nearest_station[0]


def main():
    """
    You can test all the functions here
    """
    #print(test_api())
    #print(get_json('https://api-v3.mbta.com/stops'))
    print(get_lat_long("Boston Commons"))
    print(get_nearest_station('42.3541047','-71.064822'))
    print(find_stop_near("Boston Commons"))


if __name__ == '__main__':
    main()
