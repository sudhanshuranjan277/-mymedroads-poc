import json
import re
from bs4 import BeautifulSoup


BASE_URL = "https://www.artemishospitals.com"


def clean(text):
    if not text:
        return ""

    return " ".join(
        text.replace("\xa0", " ").split()
    )


def extract_jsonld(soup):

    data = {}

    scripts = soup.find_all(
        "script",
        type="application/ld+json"
    )

    for script in scripts:

        try:

            obj = json.loads(script.string)

            if isinstance(obj, list):
                items = obj
            else:
                items = [obj]


            for item in items:

                if item.get("@type") == "Hospital":

                    data["hospital_name"] = item.get(
                        "name",
                        ""
                    )

                    data["website"] = item.get(
                        "url",
                        ""
                    )


                    data["overview"] = item.get(
                        "description",
                        ""
                    )


                    data["images"] = item.get(
                        "image",
                        ""
                    )


                    data["contact_details"] = item.get(
                        "telephone",
                        ""
                    )


                    address = item.get(
                        "address",
                        {}
                    )


                    if isinstance(address, dict):

                        data["address"] = clean(
                            f"""
                            {address.get('streetAddress','')}
                            {address.get('addressLocality','')}
                            {address.get('addressRegion','')}
                            {address.get('postalCode','')}
                            """
                        )


        except Exception:

            continue


    return data



def extract_meta_description(soup):

    tag = soup.find(
        "meta",
        attrs={
            "name": "description"
        }
    )


    if tag:

        return clean(
            tag.get("content","")
        )


    return ""



def extract_centres_of_excellence(soup):

    centres = []


    text = soup.get_text(
        "\n",
        strip=True
    )


    keywords = [

        "Emergency & Trauma Centre",
        "Heart Centre",
        "Cancer Centre",
        "Neurosciences Centre",
        "Joint Replacement",
        "Transplant Centre",
        "Women & Child Centre",
        "Pulmonology & Critical Care Centre",
        "Gastrosciences Centre"

    ]


    for item in keywords:

        if item.lower() in text.lower():

            centres.append(
                item
            )


    return ", ".join(
        centres
    )



def extract_emergency(soup):

    text = soup.get_text(
        " ",
        strip=True
    )


    if "Emergency" in text or "Trauma" in text:

        return "24x7 Emergency & Trauma Services"


    return ""



def extract_international_services(soup):

    text = soup.get_text(
        " ",
        strip=True
    )


    if "International Patient" in text:

        return "International Patient Services available"


    return ""



def extract_awards(soup):

    text = soup.get_text(
        "\n",
        strip=True
    )

    lines = [
        clean(x)
        for x in text.split("\n")
    ]

    awards = []

    ignore = [
        "Awards",
        "Awards and Accreditations",
        "Accreditations"
    ]

    for line in lines:

        if "award" in line.lower():

            if line not in ignore and len(line) > 20:

                awards.append(line)

    return ", ".join(
        list(set(awards))
    )



def scrape_hospital():

    with open(
        "output/page.html",
        "r",
        encoding="utf-8"
    ) as f:

        html = f.read()



    soup = BeautifulSoup(
        html,
        "html.parser"
    )



    hospital = {

        "hospital_id": 1,

        "hospital_name": "",

        "location": "",

        "address": "",

        "contact_details": "",

        "website": BASE_URL,

        "overview": "",

        "accreditations": "",

        "number_of_beds": "",

        "centres_of_excellence": "",

        "infrastructure": "",

        "emergency_services": "",

        "international_patient_services": "",

        "images": "",

        "awards": ""

    }



    # JSON-LD extraction

    hospital.update(
        extract_jsonld(soup)
    )



    # Meta fallback

    if not hospital["overview"]:

        hospital["overview"] = extract_meta_description(
            soup
        )



    # Location

    text = soup.get_text(
        " ",
        strip=True
    )


    if "Gurgaon" in text:

        hospital["location"] = "Gurgaon, Haryana"



    # Centres

    hospital["centres_of_excellence"] = (
        extract_centres_of_excellence(soup)
    )



    # Emergency

    hospital["emergency_services"] = (
        extract_emergency(soup)
    )



    # International Patients

    hospital["international_patient_services"] = (
        extract_international_services(soup)
    )



    # Awards

    hospital["awards"] = (
        extract_awards(soup)
    )



    # Beds

    beds = re.search(
        r"(\d+\+?\s*beds)",
        text,
        re.I
    )


    if beds:

        hospital["number_of_beds"] = beds.group(1)



    return [
        hospital
    ]