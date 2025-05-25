import requests
from dadata import Dadata
from urllib.parse import quote



API_2GIS = "02ae6139-94f3-4ea9-8858-ba50d49e463a"
API_DADATA = "9438965475222db596cee1d7b1e67fcdcaf101d2"
SECRET_DADATA = "37ed6bda2935c2b54d00b267489447c09163686e"


def geocode_to_coords(api_key, text):
    url = f"https://catalog.api.2gis.com/3.0/items/geocode?q={text}&key={api_key}&fields=items.point"
    response = requests.get(url).json()
    return response["result"]["items"][0]["point"]

def geocode_to_id(api_key, text):
    url = f"https://catalog.api.2gis.com/3.0/items/geocode?q={text}&key={api_key}&fields=items.point"
    response = requests.get(url).json()
    return response["result"]["items"][0]["id"]


def point_to_url(location):
    loc_str = f"{location['lon']},{location['lat']}"
    return quote(loc_str)





def get_count_business(api_key, id): #количество организаций в здании
    url = f"https://catalog.api.2gis.com/3.0/items?building_id={id}&key={api_key}"
    try:
        response = requests.get(url).json()
        return len(response["result"]["items"])
    except KeyError:
        return 0


def get_has_business(api_key, id): #флаг, есть ли хоть один юрлицо на точке.
    url = f"https://catalog.api.2gis.com/3.0/items?building_id={id}&key={api_key}"
    try:
        response = requests.get(url).json()
        return len(response["result"]["items"]) > 0
    except KeyError:
        return False


def get_cadastral_number(text): #получение кадастра
    dadata = Dadata(API_DADATA, SECRET_DADATA)
    result = dadata.clean("address", text)
    return result["house_cadnum"]

    
def get_property_type(kad_number): #получение типа по кадастру
    url = f"https://ns2.mapbaza.ru/api/geoportal/v2/search/geoportal?query={kad_number}"
    response = requests.get(url)
    data = response.json()
    try:
        return data["data"]["features"][0]["properties"]["options"]["purpose"]
    except (KeyError, TypeError):
        return None
    
def final_get(text):
    return {
        'name': text,
        'type': get_property_type(get_cadastral_number(text)),
        'kad': get_cadastral_number(text),
        'cnt_biz': get_count_business(API_2GIS, geocode_to_id(API_2GIS, text))
    }


    

# text = "Краснодар Северная 405"
# print(final_get(text))


# id = geocode_to_id(API_2GIS, text)
# # print(point_to_url(geocode_to_coords(API_2GIS, "Западная 8 Тимашевск")))
# print(text)
# print("Кадастровый номер:",get_cadastral_number(text))
# print("Тип:",get_property_type(get_cadastral_number(text)))
# print("Есть ли бизнесы поблизости:", get_has_business(API_2GIS, id))
# print("Количество организааций в здании:",get_count_business(API_2GIS, id))
