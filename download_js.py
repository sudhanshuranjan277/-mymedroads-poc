import requests

url = "https://www.artemishospitals.com/assets/js/doctor-listing.js"

response = requests.get(url)

with open("output/doctor-listing.js", "wb") as f:
    f.write(response.content)

print("✅ doctor-listing.js downloaded successfully.")