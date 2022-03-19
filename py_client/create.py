import requests
from requests.api import get

endpoint = "http://127.0.0.1:8000/api/deposit"

data = {
    'mobile_number': "+639552903236",
    "credits_earned": 3,
    "number_of_bottles": 12
}

get_response = requests.post(endpoint, json=data)
print(type(data['credits_earned']))
print(get_response.json())
