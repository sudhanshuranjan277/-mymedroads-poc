import requests
from bs4 import BeautifulSoup

from config.config_loader import load_config


config = load_config()


BASE_URL = config["base_url"]

HOSPITAL_ID = config["hospital"]["id"]

HOSPITAL_NAME = config["hospital"].get(
    "name",
    "Artemis Hospitals"
)


DOCTOR_API = (
    BASE_URL +
    "/common.aspx/AllDoctorsAndSpecialityListForIndex"
)


REQUEST_CONFIG = config["request"]



def clean(text):

    if not text:
        return ""

    return " ".join(
        text.replace(
            "\xa0",
            " "
        ).split()
    )





def scrape_doctors():

    """
    Fetch all doctors from Artemis API.
    Returns only valid doctor profile URLs.
    """



    headers = {

        "Content-Type":
        "application/json; charset=utf-8",

        "User-Agent":
        REQUEST_CONFIG["user_agent"]

    }



    payload = {

        "prefix": ""

    }



    try:

        response = requests.post(

            DOCTOR_API,

            headers=headers,

            json=payload,

            timeout=REQUEST_CONFIG["timeout"]

        )


    except requests.RequestException as e:


        print(
            "❌ Doctor API Error:",
            e
        )

        return []





    if response.status_code != 200:


        print(

            "❌ Doctor API failed:",
            response.status_code

        )

        return []





    data = response.json()


    doctors_html = data.get(
        "d",
        []
    )



    print(
        "API doctors received:",
        len(doctors_html)
    )



    doctors = []

    seen_urls = set()


    doctor_id = 1



    for item in doctors_html:


        soup = BeautifulSoup(

            item,

            "html.parser"

        )


        anchor = soup.find(
            "a"
        )



        if not anchor:

            continue



        href = anchor.get(
            "href",
            ""
        )



        if not href:

            continue



        href_lower = href.lower()



        # Only doctor profiles

        if "/doctor/profile/" not in href_lower:

            continue




        profile_url = (

            BASE_URL + href

            if href.startswith("/")

            else href

        )



        profile_url = profile_url.strip()



        # Remove Raipur profiles

        if "/raipur/" in profile_url.lower():

            continue



        # Remove duplicate URLs

        if profile_url in seen_urls:

            continue



        seen_urls.add(
            profile_url
        )



        doctor_name = clean(

            anchor.get_text(

                " ",

                strip=True

            )

        )



        doctor_name = doctor_name.replace(

            "[Doctor]",

            ""

        ).strip()



        # Remove invalid entries

        if not doctor_name:

            continue



        if not doctor_name.lower().startswith(

            ("dr.", "dr ")

        ):

            continue




        doctors.append({

            "doctor_id":

                doctor_id,


            "hospital_id":

                HOSPITAL_ID,


            "hospital_name":

                HOSPITAL_NAME,


            "doctor_name":

                doctor_name,


            "specialty":

                "",


            "profile_url":

                profile_url


        })



        doctor_id += 1




    print(

        "Total doctors extracted:",

        len(doctors)

    )



    return doctors