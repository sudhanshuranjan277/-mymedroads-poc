import json
import re
import requests

from bs4 import BeautifulSoup



BASE_URL = "https://www.artemishospitals.com"



HEADERS = {

    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

}



REQUEST_TIMEOUT = 30





def clean(text):

    if not text:

        return ""


    return " ".join(

        str(text)
        .replace("\xa0", " ")
        .split()

    )





def extract_jsonld(soup):

    data = {}


    for script in soup.find_all(
        "script",
        type="application/ld+json"
    ):


        try:

            obj = json.loads(
                script.get_text(
                    strip=True
                )
            )


        except Exception:

            continue



        items = (

            obj

            if isinstance(obj, list)

            else

            [obj]

        )



        for item in items:


            if not isinstance(item, dict):

                continue



            obj_type = item.get(
                "@type",
                ""
            )


            if isinstance(obj_type, list):

                obj_type = ",".join(
                    obj_type
                )



            if not any(

                x in obj_type

                for x in [

                    "Hospital",
                    "MedicalOrganization",
                    "Organization"

                ]

            ):

                continue



            name = clean(

                item.get(
                    "name",
                    ""
                )

            )


            url = clean(

                item.get(
                    "url",
                    ""
                )

            )



            # Skip Raipur hospital (Artemis Shanti Hospital, Raipur)

            if (

                "raipur" in name.lower()

                or

                "raipur" in url.lower()

            ):

                continue



            # Only keep Artemis Gurgaon (skip unrelated orgs/hospitals)

            if "artemis" not in name.lower():

                continue



            data["hospital_name"] = name



            data["website"] = url



            data["overview"] = clean(

                item.get(
                    "description",
                    ""
                )

            )



            data["contact_details"] = clean(

                item.get(
                    "telephone",
                    ""
                )

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



            image = item.get(
                "image",
                ""
            )


            if isinstance(image, list):

                image = ",".join(
                    image
                )


            data["images"] = clean(
                image
            )


    return data





def extract_meta_description(soup):

    tag = soup.find(

        "meta",

        attrs={

            "name":
                "description"

        }

    )


    if tag:

        return clean(

            tag.get(
                "content",
                ""
            )

        )


    return ""





def extract_images(soup):

    images = []


    ignore_keywords = [

        "icon",

        "logo",

        "captcha",

        "loader",

        "whatsapp",

        "appstore",

        "playstore",

        "flag",

        "googleusercontent"

    ]



    allowed_keywords = [

        "hospital",

        "technology",

        "facility",

        "infrastructure",

        "gallery",

        "award",

        "img"

    ]



    for img in soup.find_all(

        "img",

        src=True

    ):


        src = img.get(
            "src",
            ""
        )


        if not src:

            continue



        if src.startswith("/"):

            src = BASE_URL + src



        src_lower = src.lower()



        # Skip Raipur-related images (blog banners, Shanti Hospital photos, etc.)

        if "raipur" in src_lower:

            continue



        if "shanti" in src_lower:

            continue



        if any(

            item in src_lower

            for item in ignore_keywords

        ):

            continue



        if not any(

            item in src_lower

            for item in allowed_keywords

        ):

            continue



        if src not in images:

            images.append(
                src
            )



    return ",".join(

        images[:20]

    )





def extract_contact_details(soup):

    text = soup.get_text(

        " ",

        strip=True

    )



    contacts = []



    phones = re.findall(

        r"(?:\+91[-\s]?)?\d{10}",

        text

    )


    contacts.extend(
        phones
    )



    emails = re.findall(

        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

        text

    )


    contacts.extend(
        emails
    )


    return ", ".join(

        list(set(contacts))

    )





def extract_accreditations(soup):

    text = soup.get_text(

        " ",

        strip=True

    ).lower()



    result = []



    if "nabh" in text:

        result.append(
            "NABH Accreditation"
        )



    if "jci" in text:

        result.append(
            "JCI Accreditation"
        )



    if "nabl" in text:

        result.append(
            "NABL Certification"
        )



    if "iso" in text:

        result.append(
            "ISO Certification"
        )



    return ", ".join(

        result

    )
def extract_number_of_beds(text):
    """Extract the hospital bed capacity when it is stated on the page."""
    patterns = (
        r"\d+\+?\s*beds",
        r"\d+\+?\s*bedded",
        r"capacity\s+of\s+\d+",
    )
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return clean(match.group())
    return ""





def extract_centres_of_excellence(soup):

    text = soup.get_text(

        " ",

        strip=True

    )


    centres = []


    keywords = [

        "Heart Centre",

        "Cardiac Sciences",

        "Cancer Centre",

        "Oncology",

        "Neurosciences",

        "Orthopaedics",

        "Joint Replacement",

        "Spine",

        "Transplant",

        "Kidney Transplant",

        "Liver Transplant",

        "Women & Child",

        "Critical Care",

        "Emergency"

    ]


    # Generic menu/navigation text that should never be treated as a centre

    ignore = [

        "Services",

        "General Information",

        "Request an Appointment",

        "Contacting Patients"

    ]



    for item in keywords:


        if item.lower() in ignore:

            continue


        if item.lower() in [
            i.lower() for i in ignore
        ]:

            continue


        if item.lower() in text.lower():

            centres.append(
                item
            )



    centres = [

        c for c in centres

        if c.lower() not in [
            i.lower() for i in ignore
        ]

    ]



    return ", ".join(

        list(set(centres))

    )





def extract_infrastructure(soup):

    text = soup.get_text(

        " ",

        strip=True

    )


    infrastructure = []


    keywords = [

        "ICU",

        "Intensive Care",

        "Modular OT",

        "Operation Theatre",

        "Operating Theatre",

        "Robotic Surgery",

        "Da Vinci",

        "Cath Lab",

        "MRI",

        "CT Scan",

        "PET CT",

        "Laboratory",

        "Pharmacy",

        "Diagnostic"

    ]



    for item in keywords:


        if item.lower() in text.lower():

            infrastructure.append(
                item
            )



    return ", ".join(

        list(set(infrastructure))

    )





def extract_emergency_services(soup):

    text = soup.get_text(

        " ",

        strip=True

    )


    services = []


    keywords = [

        "24x7 Emergency",

        "Emergency",

        "Trauma Centre",

        "Ambulance",

        "Critical Care",

        "Emergency Care"

    ]



    for item in keywords:


        if item.lower() in text.lower():

            services.append(
                item
            )



    return ", ".join(

        list(set(services))

    )





def extract_international_services(soup):

    text = soup.get_text(

        " ",

        strip=True

    ).lower()


    services = []


    mapping = {

        "international patient":

            "International Patient Services",


        "medical interpreter":

            "Medical Interpreter Services",


        "interpreter":

            "Medical Interpreter Services",


        "visa":

            "Visa Assistance",


        "airport pickup":

            "Airport Pickup",


        "accommodation":

            "Accommodation Assistance",


        "travel assistance":

            "Travel Assistance"

    }



    for key, value in mapping.items():


        if key in text:

            services.append(
                value
            )



    return ", ".join(

        list(set(services))

    )





def extract_awards(soup):

    text = soup.get_text(

        "\n",

        strip=True

    )


    awards = []


    keywords = [

        "award",

        "awarded",

        "achievement",

        "recognition",

        "ranked"

    ]



    for line in text.split("\n"):


        line = clean(
            line
        )


        if not line:

            continue



        # Skip lines referencing Raipur/Shanti so unrelated awards don't leak in

        if "raipur" in line.lower() or "shanti" in line.lower():

            continue



        if any(

            word in line.lower()

            for word in keywords

        ):


            if len(line) > 25:

                awards.append(
                    line
                )



    return ", ".join(

        list(set(awards[:10]))

    )





def scrape_hospital():


    response = requests.get(

        BASE_URL,

        headers=HEADERS,

        timeout=REQUEST_TIMEOUT

    )



    if response.status_code != 200:


        print(

            "❌ Hospital request failed:",

            response.status_code

        )


        return []



    soup = BeautifulSoup(

        response.text,

        "html.parser"

    )



    text = soup.get_text(

        " ",

        strip=True

    )



    hospital = {


        "hospital_id":

            1,


        "hospital_name":

            "Artemis Hospitals",


        "location":

            "Gurgaon, Haryana",


        "address":

            "",


        "contact_details":

            "",


        "website":

            BASE_URL,


        "overview":

            "",


        "accreditations":

            "",


        "number_of_beds":

            "",


        "centres_of_excellence":

            "",


        "infrastructure":

            "",


        "emergency_services":

            "",


        "international_patient_services":

            "",


        "images":

            "",


        "awards":

            ""

    }





    # JSON-LD — only apply if it resolved to the Gurgaon hospital, not Raipur

    json_data = extract_jsonld(
        soup
    )


    if json_data.get("hospital_name"):

        if "raipur" not in json_data["hospital_name"].lower():

            hospital.update(
                json_data
            )



    if not hospital["overview"]:


        hospital["overview"] = extract_meta_description(
            soup
        )



    if not hospital["address"]:


        hospital["address"] = (

            "Artemis Hospitals, "
            "Sector 51, "
            "Gurugram, Haryana, India"

        )


    # Safety net: never let a Raipur address slip through, even from JSON-LD

    if "raipur" in hospital["address"].lower():

        hospital["address"] = (

            "Artemis Hospitals, "
            "Sector 51, "
            "Gurugram, Haryana, India"

        )


    # Safety net: force correct website/name regardless of what JSON-LD returned

    if "raipur" in hospital["website"].lower():

        hospital["website"] = BASE_URL


    if "raipur" in hospital["hospital_name"].lower() or "shanti" in hospital["hospital_name"].lower():

        hospital["hospital_name"] = "Artemis Hospitals"



    if not hospital["contact_details"]:


        hospital["contact_details"] = extract_contact_details(
            soup
        )



    hospital["images"] = extract_images(
        soup
    )



    hospital["accreditations"] = extract_accreditations(
        soup
    )



    hospital["number_of_beds"] = extract_number_of_beds(
        text
    )



    hospital["centres_of_excellence"] = extract_centres_of_excellence(
        soup
    )



    hospital["infrastructure"] = extract_infrastructure(
        soup
    )



    hospital["emergency_services"] = extract_emergency_services(
        soup
    )



    hospital["international_patient_services"] = extract_international_services(
        soup
    )



    hospital["awards"] = extract_awards(
        soup
    )



    return [

        hospital

    ]