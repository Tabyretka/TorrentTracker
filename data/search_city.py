import requests


def get_city_coord(addr):
    toponym_to_find = addr
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        pass
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return ",".join([toponym_longitude, toponym_lattitude])


def get_city_pic(coords):
    delta = "0.5"
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    return f"{map_api_server}?ll={coords}&spn={','.join([delta, delta])}&l=map"

