import requests
import json


url = "https://www.artemishospitals.com/common.aspx/AllDoctorsAndSpecialityListForIndex"


payload = {
    "prefix": ""
}


headers = {
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "Mozilla/5.0"
}


response = requests.post(
    url,
    headers=headers,
    data=json.dumps(payload)
)


print("Status:", response.status_code)

print(response.text[:1000])