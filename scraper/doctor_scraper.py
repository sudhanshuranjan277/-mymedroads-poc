import re
from bs4 import BeautifulSoup

BASE_URL = "https://www.artemishospitals.com"


def scrape_doctors():
    with open("output/page.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Extract HTML from JavaScript
    match = re.search(
        r"container\.innerHTML\s*=\s*`(.*?)`;",
        html,
        re.DOTALL
    )

    if not match:
        print("❌ Doctor HTML block not found.")
        return []

    doctor_html = match.group(1)

    soup = BeautifulSoup(doctor_html, "html.parser")

    cards = soup.select("div.doctor-container")

    print(f"Total doctor cards: {len(cards)}")

    # Debug
    names = [
        c.select_one(".name").get_text(strip=True)
        for c in cards
        if c.select_one(".name")
    ]

    print("Total names extracted:", len(names))
    print("Unique names:", len(set(names)))

    duplicates = {}
    for name in names:
        duplicates[name] = duplicates.get(name, 0) + 1

    dup_names = {k: v for k, v in duplicates.items() if v > 1}

    if dup_names:
        print("\nDuplicate Doctors:")
        for name, count in dup_names.items():
            print(f"{name} -> {count}")
    else:
        print("\nNo duplicate doctor names found.")

    doctors = []

    for i, card in enumerate(cards, start=1):

        name = card.select_one(".name")
        specialty = card.select_one(".specialty")

        profile_url = ""
        appointment_url = ""

        for a in card.select("a[href]"):
            href = a.get("href", "")

            if "/doctor/profile/" in href:
                profile_url = BASE_URL + href

            elif "/make-an-apointment" in href:
                appointment_url = BASE_URL + href

        doctors.append({
            "doctor_id": i,
            "hospital_id": 1,
            "doctor_name": name.get_text(strip=True) if name else "",
            "specialty": specialty.get_text(strip=True) if specialty else "",
            "profile_url": profile_url,
            "appointment_url": appointment_url,
        })

    return doctors