import os
import json
import requests
from dotenv import load_dotenv
from geopy import distance
from pprint import pprint


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def main():
    load_dotenv()
    apikey = os.getenv("Key")
    if not apikey:
        print("Ошибка: не найден API ключ в файле .env")
        return
    
    with open("coffee.json", "r", encoding="CP1251") as my_file:
        coffee_json = my_file.read()
        file_content = json.loads(coffee_json)
    
    user_address = input("Где вы находитесь? ")
    user_coords = fetch_coordinates(apikey, user_address)
    
    coffee_list = []
    for coffee in file_content :
        coffee_name = coffee["Name"]
        coffee_lat = float(coffee["Latitude_WGS84"])
        coffee_lon = float(coffee["Longitude_WGS84"])
        coffee_coords = (coffee_lat, coffee_lon)
        dist = distance.distance(user_coords, coffee_coords).km
    
        coffee_list.append({
            "title" : coffee_name,
            "distance" : round(dist, 2),
            "latitude" : (coffee_lat),
            "longitude" : (coffee_lon)
            })
    
    print("Ваши координаты", user_coords)
    pprint(coffee_list)


if __name__ == '__main__':
    main()
