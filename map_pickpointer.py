import random
import csv
import requests
import json
from math import *


def place_generate():
    # генерация рандомного названия города в России
    lst = []
    with open("data/city.csv", mode="r", encoding='utf-8') as cities:
        reader = csv.reader(cities, delimiter=',', quotechar='"')
        return random.choice(list([i[0] for i in reader]))


print(place_generate())


def get_coordinates(city_name):
    # получение координат города по названию
    try:
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            'geocode': city_name,
            'format': 'json'
        }
        response = requests.get(url, params)
        json = response.json()
        coordinates_str = json['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']['Point']['pos']
        long, lat = map(float, coordinates_str.split())
        return long, lat
    except Exception as e:
        return e


def get_country(city_name):
    """Получаем страну города (для возможного расширения работы на другие страны)"""
    try:
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            'geocode': city_name,
            'format': 'json'
        }
        data = requests.get(url, params).json()
        return data['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']['metaDataProperty'][
            'GeocoderMetaData']['AddressDetails']['Country']['CountryName']
    except Exception as e:
        return e


def get_distance(p1, p2):
    """определяем насколько далеко две точки"""
    """нужно для последующей выдачи очков за игру"""
    R = 6373.0

    lon1 = radians(p1[0])
    lat1 = radians(p1[1])
    lon2 = radians(p2[0])
    lat2 = radians(p2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance
