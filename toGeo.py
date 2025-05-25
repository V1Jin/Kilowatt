import json
from external_data import geocode_to_coords
import sys

sys.stdout.reconfigure(encoding='utf-8')


def color_point(percent):
    if (percent <= 40) :
        return './ico/location-dot-solid(3).png'
    elif (percent <= 65): 
        return './ico/location-dot-solid(2).png'
    elif (percent <= 85): 
        return './ico/location-dot-solid(1).png'
    return './ico/location-dot-solid.png';
    

API_2GIS = "f93a5b47-6e3b-4c23-ba03-185daa02ef64"


with open('dataset_train.json', 'r', encoding='utf-8') as f:
    input_data = json.load(f)

# Преобразование в GeoJSON
geojson = {
    "type": "FeatureCollection",
    "features": []
}

for item in input_data:
    print(item["address"])
    coordinates = geocode_to_coords(API_2GIS,item["address"])
    
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [coordinates["lon"], coordinates["lat"]],
        },
        "properties": {
            "icon": color_point(float(item["prediction"])),
            "accountId": item["accountId"],
            "isCommercial": item["isCommercial"],
            "address": item["address"],
            "buildingType": item["buildingType"],
            "prediction": item["prediction"]
        }
    }
    
    geojson["features"].append(feature)

with open('output.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson, f, indent=2, ensure_ascii=False)

print("результат сохранён в output.geojson")