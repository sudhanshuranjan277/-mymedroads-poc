"""
Artemis Hospital Doctor Profile Scraper

Extracts:
- Doctor Name
- Designation
- Department
- Specialty
- Qualification
- Experience
- Expertise
- Procedures
- Memberships
- Languages
- Publications
- Awards
- Summary
- Profile Image
"""

import json
import re
import html

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin



BASE_URL = "https://www.artemishospitals.com"


HEADERS = {

    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",

    "Accept-Language":
        "en-US,en;q=0.9"

}


REQUEST_TIMEOUT = 30
MAX_RETRIES = 3



PROFILE_FIELDS = (

    "hospital_name",

    "doctor_name",

    "designation",

    "department",

    "specialty",

    "qualification",

    "experience",

    "expertise",

    "procedures_performed",

    "professional_memberships",

    "languages",

    "publications",

    "awards",

    "consultation_location",

    "summary",

    "profile_photo",

)



CONTENT_LABELS = (

    "Qualifications",
    "Qualification",
    "Education",
    "Educational Qualification",
    "Academic Qualification",
    "Medical Education",
    "Degrees",

    "Brief Profile",
    "Profile",

    "Work Experience",
    "Professional Experience",
    "Clinical Experience",
    "Experience",
    "Years of Experience",

    "Areas of Expertise",
    "Area of Interest",
    "Clinical Focus",
    "Special Interest",
    "Expertise",
    "Specialization",
    "Field of Expertise",

    "Procedures Performed",
    "Procedures",
    "Treatments",
    "Clinical Procedures",

    "Professional Memberships",
    "Memberships",
    "Membership",

    "Publications",
    "Research Publications",
    "Scientific Publications",
    "Research",

    "Awards",
    "Honors and Awards",
    "Honours and Awards",
    "Achievements",

    "Languages",
    "Languages Spoken",

)





def normalize_text(text):

    """
    Common text cleaning.
    """

    if not text:
        return ""


    value = html.unescape(
        str(text)
    )


    value = value.replace(
        "\xa0",
        " "
    )


    replacements = {

        "Air ForceMedicalCollege":
            "Air Force Medical College",

        "MedicalCollege":
            "Medical College",

        "BombayUniversity":
            "Bombay University",

        "DelhiUniversity":
            "Delhi University",

        "MedicalCouncil":
            "Medical Council",

        "ofMedical":
            "of Medical",

        "years ofexperience":
            "years of experience"

    }


    for old, new in replacements.items():

        value = value.replace(
            old,
            new
        )


    # 18years -> 18 years

    value = re.sub(

        r"(\d+)years",

        r"\1 years",

        value,

        flags=re.I

    )


    value = re.sub(

        r",(?=\S)",

        ", ",

        value

    )


    return " ".join(
        value.split()
    )





def clean(text):

    return normalize_text(text)





def clean_department_value(text):

    """
    Remove unwanted labels.
    """

    if not text:
        return ""


    remove_values = [

        "Designation:",
        "Designation",

        "Department:",
        "Department",

        "Specialty:",
        "Specialty",

        "Speciality:",
        "Speciality"

    ]


    for item in remove_values:

        text = text.replace(
            item,
            ""
        )


    return clean(text)





def _clean_name(name):

    """
    Clean doctor name.
    """

    if not name:

        return ""


    name = clean(name)


    name = name.replace(
        "[Doctor]",
        ""
    )


    name = re.split(

        r"\s*(?:\||\s-\s|\sat\s)",

        name,

        maxsplit=1,

        flags=re.I

    )[0]


    return clean(name)





def find_text_by_id_suffix(
        soup,
        suffix
):

    element = soup.find(

        id=re.compile(

            re.escape(suffix) + r"$",

            re.I

        )

    )


    if element:

        return clean(

            element.get_text(

                " ",

                strip=True

            )

        )


    return ""





def find_text_by_class(
        soup,
        selector
):

    element = soup.select_one(
        selector
    )


    if element:

        return clean(

            element.get_text(

                " ",

                strip=True

            )

        )


    return ""





def get_meta(
        soup,
        name=None,
        prop=None
):

    attrs = (

        {"name": name}

        if name

        else

        {"property": prop}

    )


    tag = soup.find(
        "meta",
        attrs=attrs
    )


    if tag:

        return clean(
            tag.get(
                "content",
                ""
            )
        )


    return ""

def extract_jsonld(soup):

    data = {}


    for script in soup.find_all(
        "script",
        type="application/ld+json"
    ):

        try:

            payload = json.loads(
                script.get_text(
                    strip=True
                )
            )

        except Exception:

            continue



        items = (

            payload

            if isinstance(payload, list)

            else

            [payload]

        )



        for item in items:


            if not isinstance(item, dict):

                continue



            candidates = []


            graph = item.get(
                "@graph",
                []
            )


            if isinstance(graph, list):

                candidates.extend(
                    graph
                )


            candidates.append(
                item
            )



            for candidate in candidates:


                if not isinstance(candidate, dict):

                    continue



                types = candidate.get(
                    "@type",
                    []
                )


                if isinstance(types, str):

                    types = [
                        types
                    ]



                if not (

                    "Person" in types

                    or

                    "Physician" in types

                ):

                    continue



                if candidate.get("name"):

                    data["doctor_name"] = clean(
                        candidate["name"]
                    )



                image = candidate.get(
                    "image",
                    ""
                )


                if isinstance(image, dict):

                    image = image.get(
                        "url",
                        ""
                    )



                if image:

                    data["profile_photo"] = clean(
                        image
                    )


    return data





def fetch_profile_html(
        profile_url,
        session=None
):

    if not profile_url:

        return ""


    client = session or requests


    url = urljoin(
        BASE_URL + "/",
        profile_url
    )


    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):

        try:

            response = client.get(

                url,

                headers=HEADERS,

                timeout=REQUEST_TIMEOUT

            )


            response.raise_for_status()


            return response.text



        except requests.RequestException as error:


            if attempt == MAX_RETRIES:

                print(

                    "Profile scrape failed:",

                    url,

                    error

                )



    return ""





def _section_text(
        soup,
        *keywords
):


    for keyword in keywords:


        value = find_text_by_id_suffix(

            soup,

            keyword

        )


        if value:

            return value



        label = soup.find(

            string=re.compile(

                rf"^\s*{re.escape(keyword)}\s*:?\s*$",

                re.I

            )

        )


        if label:


            parent = label.parent


            if parent:


                sibling = parent.find_next_sibling()


                target = sibling or parent


                value = clean(

                    target.get_text(

                        " ",

                        strip=True

                    )

                )


                if value.lower() != keyword.lower():

                    return value



    return ""





def _content_sections(soup):


    content = find_text_by_id_suffix(

        soup,

        "LabelContent"

    )


    if not content:

        return {}



    labels = "|".join(

        re.escape(label)

        for label in CONTENT_LABELS

    )



    parts = re.split(

        rf"(?i)\b({labels})\s*:?\s*",

        content

    )



    result = {}



    for label, value in zip(

        parts[1::2],

        parts[2::2]

    ):


        value = clean(
            value
        )


        if value:

            result[
                label.lower()
            ] = value



    return result





def _first_section(
        sections,
        *labels
):


    for label in labels:


        value = sections.get(

            label.lower(),

            ""

        )


        if value:

            return value



    return ""





def extract_from_text(
        text,
        keywords
):


    output = []



    for keyword in keywords:


        pattern = (

            rf"{keyword}"

            r"\s*[:\-]?\s*"

            r"(.*?)(?="

            r"Clinical Focus|"

            r"Field of Specialization|"

            r"Professional Membership|"

            r"Publications|"

            r"Research|"

            r"Awards|"

            r"Honors|"

            r"$)"

        )


        match = re.search(

            pattern,

            text,

            re.I | re.S

        )



        if match:


            value = clean(

                match.group(1)

            )


            if value:

                output.append(
                    value
                )



    return ", ".join(
        list(set(output))
    )





def extract_fallback_from_text(page_text):

    """
    Level-3 fallback: when labelled sections are missing entirely,
    pull qualification / experience / expertise / languages straight
    out of the raw profile text using patterns commonly seen on
    unlabelled Artemis doctor pages.
    """

    data = {}


    # Qualification fallback

    qualification_patterns = [

        r"(MBBS.*?(?:MD|MS|DM|MCh|DNB).*?)(?=\s+\d+\s+years|\s+Experience|$)",

        r"(Bachelor.*?(?:Medicine|Surgery).*?)",

        r"(MD.*?)(?=\s+\d+\s+years|$)",

        r"(MS.*?)(?=\s+\d+\s+years|$)",

        r"(DM.*?)(?=\s+\d+\s+years|$)"

    ]


    for pattern in qualification_patterns:

        match = re.search(
            pattern,
            page_text,
            re.I
        )

        if match:

            data["qualification"] = normalize_text(
                match.group()
            )

            break



    # Experience fallback

    exp_match = re.search(

        r"(\d+\+?\s*(?:years?|yrs?)(?:\s+of\s+experience)?)",

        page_text,

        re.I

    )


    if exp_match:

        data["experience"] = normalize_text(
            exp_match.group()
        )



    # Expertise fallback

    expertise_keywords = [

        "Clinical Focus",

        "Special Interest",

        "Area of Interest",

        "Expertise",

        "Specialization"

    ]


    for keyword in expertise_keywords:


        pattern = (

            keyword +

            r"\s*[:\-]?\s*(.*?)(?=\s+(?:Awards|Membership|Experience|Education)|$)"

        )


        match = re.search(

            pattern,

            page_text,

            re.I

        )


        if match:


            data["expertise"] = normalize_text(

                match.group(1)

            )

            break



    # Languages fallback


    language_match = re.search(

        r"(Languages?|Languages Spoken)\s*[:\-]?\s*(.*?)(?=\s+(?:Awards|Experience|Qualification)|$)",

        page_text,

        re.I

    )


    if language_match:


        data["languages"] = normalize_text(

            language_match.group(2)

        )


    return data





def extract_procedures(text):


    keywords = [

        "Angioplasty",

        "Replacement",

        "Transplant",

        "Surgery",

        "Surgical",

        "Procedure",

        "Treatment",

        "Arthroplasty"

    ]



    found = []



    for sentence in text.split("."):


        for word in keywords:


            if word.lower() in sentence.lower():

                found.append(
                    clean(sentence)
                )



    return ", ".join(

        list(set(found[:10]))

    )





def extract_publications(text):


    patterns = [

        r"\d+\+?\s*Scientific publications",

        r"\d+\+?\s*publications",

        r"Published.*",

        r"Research.*"

    ]



    for pattern in patterns:


        match = re.search(

            pattern,

            text,

            re.I

        )


        if match:

            return clean(
                match.group()
            )



    return ""
def scrape_doctor_profile(
        profile_url,
        session=None
):


    result = dict.fromkeys(
        PROFILE_FIELDS,
        ""
    )


    result["hospital_name"] = (
        "Artemis Hospitals"
    )


    html_content = fetch_profile_html(
        profile_url,
        session=session
    )


    if not html_content:

        return result



    soup = BeautifulSoup(
        html_content,
        "html.parser"
    )


    page_text = clean(
        soup.get_text(
            " ",
            strip=True
        )
    )


    text_fallback = extract_fallback_from_text(
        page_text
    )


    sections = _content_sections(
        soup
    )



    # JSON-LD

    result.update(
        extract_jsonld(
            soup
        )
    )



    # -------------------------
    # Doctor Name
    # -------------------------

    result["doctor_name"] = _clean_name(

        find_text_by_id_suffix(
            soup,
            "LabelName"
        )

        or

        find_text_by_class(
            soup,
            "h1"
        )

        or

        get_meta(
            soup,
            prop="og:title"
        )

        or

        result["doctor_name"]

    )



    # -------------------------
    # Designation
    # -------------------------

    result["designation"] = (

        find_text_by_id_suffix(
            soup,
            "LabelDesignation"
        )

        or

        find_text_by_id_suffix(
            soup,
            "LabelDepartment"
        )

        or

        _section_text(
            soup,
            "Designation"
        )

    )



    result["designation"] = clean(
        result["designation"]
    )



    # -------------------------
    # Department
    # -------------------------

    department = (

        _first_section(
            sections,
            "Department",
            "Speciality",
            "Specialty"
        )

        or

        _section_text(
            soup,
            "Department",
            "Speciality",
            "Specialty"
        )

    )



    department = clean_department_value(
        department
    )


    if department in [

        "",
        "Designation",
        "Designation:"

    ]:

        department = clean_department_value(
            result["designation"]
        )



    result["department"] = department


    result["specialty"] = department



    # -------------------------
    # Qualification
    # -------------------------

    result["qualification"] = (

        _first_section(
            sections,
            "Qualifications",
            "Qualification",
            "Education",
            "Educational Qualification",
            "Academic Qualification",
            "Medical Education",
            "Degrees"
        )

        or

        _section_text(
            soup,
            "LabelQualification",
            "Qualifications",
            "Qualification",
            "Education",
            "Education Qualification"
        )

    )


    if not result["qualification"]:

        result["qualification"] = text_fallback.get(
            "qualification",
            ""
        )



    # -------------------------
    # Experience
    # -------------------------

    result["experience"] = (

        _first_section(
            sections,
            "Years of Experience",
            "Work Experience",
            "Professional Experience",
            "Clinical Experience",
            "Experience"
        )

        or

        _section_text(
            soup,
            "Experience",
            "WorkExperience",
            "Years"
        )

    )



    if not result["experience"]:

        match = re.search(

            r"\b\d+\+?\s*(?:years?|yrs?)(?:\s+of\s+experience)?\b",

            page_text,

            re.I

        )


        if match:

            result["experience"] = clean(
                match.group()
            )



    if not result["experience"]:

        result["experience"] = text_fallback.get(
            "experience",
            ""
        )



    # -------------------------
    # Expertise
    # -------------------------

    result["expertise"] = (

        _first_section(
            sections,
            "Areas of Expertise",
            "Area of Interest",
            "Clinical Focus",
            "Special Interest",
            "Expertise",
            "Specialization",
            "Field of Expertise"
        )

        or

        _section_text(
            soup,
            "Expertise",
            "ClinicalFocus",
            "SpecialInterest"
        )

        or

        extract_from_text(
            page_text,
            [
                "Clinical Focus",
                "Field of Specialization",
                "Special Interest",
                "Expertise"
            ]
        )

    )


    if not result["expertise"]:

        result["expertise"] = text_fallback.get(
            "expertise",
            ""
        )



    # -------------------------
    # Procedures
    # -------------------------

    result["procedures_performed"] = (

        _first_section(
            sections,
            "Procedures",
            "Procedures Performed"
        )

        or

        extract_procedures(
            page_text
        )

    )



    # -------------------------
    # Membership
    # -------------------------

    result["professional_memberships"] = (

        _first_section(
            sections,
            "Professional Memberships",
            "Memberships",
            "Membership"
        )

        or

        _section_text(
            soup,
            "Membership",
            "Association"
        )

    )



    # -------------------------
    # Languages
    # -------------------------

    result["languages"] = (

        _section_text(
            soup,
            "LabelLanguagesValue",
            "Languages",
            "Language",
            "Languages Spoken"
        )

        or

        _first_section(
            sections,
            "Languages",
            "Languages Spoken"
        )

    )


    if not result["languages"]:

        result["languages"] = text_fallback.get(
            "languages",
            ""
        )



    # -------------------------
    # Publications
    # -------------------------

    result["publications"] = (

        _first_section(
            sections,
            "Publications",
            "Research Publications"
        )

        or

        extract_publications(
            page_text
        )

    )



    # -------------------------
    # Awards
    # -------------------------

    result["awards"] = (

        _first_section(
            sections,
            "Awards",
            "Honors and Awards",
            "Honours and Awards"
        )

        or

        extract_from_text(
            page_text,
            [
                "Awards",
                "Honors",
                "Achievements",
                "Recognition",
                "Commendation"
            ]
        )

    )



    # -------------------------
    # Summary
    # -------------------------

    result["summary"] = (

        get_meta(
            soup,
            prop="og:description"
        )

        or

        _first_section(
            sections,
            "Brief Profile"
        )

        or

        _section_text(
            soup,
            "Brief Profile",
            "Profile"
        )

    )



    # -------------------------
    # Consultation Location
    # -------------------------

    result["consultation_location"] = (
        "Artemis Hospitals, Gurgaon"
    )



    # -------------------------
    # Profile Image
    # -------------------------

    photo = ""


    for img in soup.find_all(
        "img",
        src=True
    ):


        src = img.get(
            "src",
            ""
        )


        src_lower = src.lower()



        if (

            "doctor" in src_lower

            or

            "doctors/photos" in src_lower

            or

            "sitefiles/doctors" in src_lower

        ):

            photo = src

            break



    result["profile_photo"] = (

        photo

        or

        get_meta(
            soup,
            prop="og:image"
        )

    )



    result["profile_photo"] = urljoin(

        BASE_URL + "/",

        result["profile_photo"]

    )



    return {

        key: clean(value)

        for key, value in result.items()

    }