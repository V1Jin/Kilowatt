import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

url = "https://kilowatt.onrender.com/external-data"

data = {
    "text": "Тимашевск Западная 8"
}

try:
    response = requests.post(url, json=data)
    response.raise_for_status()  

    print("Успешный ответ:")
    print(response.json())

except requests.exceptions.RequestException as e:
    print("Ошибка при запросе:")
    print(e)
