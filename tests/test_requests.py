import requests
from pathlib import Path

url = "https://www.artemishospitals.com/doctor"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print(f"Status Code: {response.status_code}")

# Save HTML for inspection
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

html_file = output_dir / "page.html"

with open(html_file, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"HTML saved to: {html_file}")