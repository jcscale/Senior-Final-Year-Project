import requests
from requests.api import get

endpoint = "http://127.0.0.1:8000/api/withdraw/"

data = {
    "mobile_number": "+639213456789",
    "pin_number": "1234",
    "amount": 2
}

get_response = requests.post(endpoint, json=data)
print(get_response.json())
