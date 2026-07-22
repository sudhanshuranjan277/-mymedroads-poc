import json
import re
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean(text):
    if not text:
        return ""
    return " ".join(text.replace("\xa0", " ").split())


def extract_jsonld_fields_via_regex(raw_text):
    """
    Fallback for when the Physician JSON-LD block is malformed (Artemis'
    site emits an extra trailing '}' on every doctor page, which breaks
    json.loads). Pulls the fields we need directly with regex instead
    of relying on the JSON being valid.
    """

    data = {}

    m = re.search(r'"image"\s*:\s*"([^"]+)"', raw_text)
    if m:
        data["profile_photo"] = m.group(1)

    m = re.search(r'"description"\s*:\s*"([^"]*)"', raw_text)
    if m:
        data["summary"] = clean(m.group(1))

    m = re.search(r'"medicalSpecialty"\s*:\s*"([^"]*)"', raw_text)
    if m:
        data["department"] = clean(m.group(1))

    return data


def extract_jsonld(soup):
    """
    Extract data from JSON-LD (Physician schema block).
    Gives us: profile_photo, summary, department (as a fallback/cross-check).
    """

    data = {}

    scripts = soup.find_all("script", type="application/ld+json")

    for script in scripts:

        raw = script.string or ""

        if '"Physician"' not in raw:
            continue

        try:

            obj = json.loads(raw)

            if isinstance(obj, list):
                objs = obj
            else:
                objs = [obj]

            for item in objs:

                if item.get("@type") == "Physician":

                    data["profile_photo"] = item.get("image", "")
                    data["summary"] = item.get("description", "")
                    data["department"] = item.get("medicalSpecialty", "")

                    return data

        except Exception:
            # The site's Physician JSON-LD block is known to sometimes
            # have an extra trailing '}', making it invalid JSON.
            # Pull the fields out directly instead of giving up.
            fallback = extract_jsonld_fields_via_regex(raw)
            if fallback:
                return fallback

    return data


# -----------------------------------------------------------------
# ASP.NET server-control ID based extraction (primary strategy)
# -----------------------------------------------------------------
# Artemis Hospitals' doctor profile pages are built on the same
# ASP.NET WebForms template for every doctor. Fields are rendered
# by server controls with consistent ID suffixes, e.g.:
#
#   <span id="m_d_Content1_LabelSpecialtyValue">Neuroanaesthesia...</span>
#   <span id="m_d_Content1_LabelLocationValue">Gurugram</span>
#   <span id="m_d_Content1_LabelLanguagesValue">English, Hindi</span>
#   <span id="m_d_Content1_LabelContent">Qualifications: ... </span>
#
# We match on the ID *suffix* (not the full ID) so this keeps working
# even if the numeric/control prefix ever changes between pages.

def find_element_by_id_suffix(soup, suffix):
    return soup.find(id=re.compile(re.escape(suffix) + r"$"))


def find_text_by_id_suffix(soup, suffix):
    tag = find_element_by_id_suffix(soup, suffix)
    return clean(tag.get_text()) if tag else ""


# Labels that appear as bold text (e.g. "Qualifications:") inside the
# single big "Profile" content block. Order doesn't matter for parsing,
# but this list should cover every variant seen across the site.
CONTENT_BLOCK_LABELS = [
    "Qualifications",
    "Qualification",
    "Work Experience",
    "Experience",
    "Years of Experience",
    "Procedures Performed",
    "Procedures",
    "Clinical Focus",
    "Areas of Expertise",
    "Area of Expertise",
    "Expertise",
    "Memberships",
    "Professional Memberships",
    "Membership",
    "Honors And Awards",
    "Honours And Awards",
    "Awards",
    "Publications",
    "Research Publications",
    "Languages",
    "Languages Spoken",
    "Consultation Timings",
]


def parse_profile_content(content_text):
    """
    The doctor "Profile" block is one big blob of pasted-from-Word HTML
    where each subsection is introduced by a bold label like
    'Qualifications:', 'Work Experience:', 'Memberships:', etc.,
    instead of separate <h2>/<h3> headings. This splits that blob into
    a dict keyed by lowercase label -> section text.
    """

    if not content_text:
        return {}

    pattern = r"(" + "|".join(re.escape(l) for l in CONTENT_BLOCK_LABELS) + r")\s*:\s*"

    parts = re.split(pattern, content_text, flags=re.IGNORECASE)

    result = {}

    # parts[0] is any preamble before the first label (usually empty/junk)
    pairs = parts[1:]

    for label, body in zip(pairs[0::2], pairs[1::2]):
        key = label.strip().lower()

        # Clean each line individually but KEEP the line breaks between
        # them -- collapsing everything to one line makes it impossible
        # to later isolate a single line (e.g. a stray publication
        # mention buried inside the Awards section).
        lines = [clean(l) for l in body.split("\n")]
        lines = [l for l in lines if l]
        value = "\n".join(lines)

        if value:
            if key not in result:
                result[key] = value
            else:
                result[key] += "\n" + value

    return result


def get_from_parsed(parsed, *label_keys):
    for key in label_keys:
        val = parsed.get(key.lower())
        if val:
            return val
    return ""


# -----------------------------------------------------------------
# Heading / label based extraction (fallback strategy)
# -----------------------------------------------------------------
# Used only when the ID-based / content-block approach above finds
# nothing for a given field -- e.g. if a page uses a different layout.

def get_section_text(soup, heading):

    heading = heading.lower()

    for tag in soup.find_all(["h2", "h3", "h4", "h5", "h6", "strong", "b", "label", "dt", "th"]):

        title = clean(tag.get_text()).lower()

        if not title:
            continue

        if heading in title:

            texts = []

            same_line = clean(tag.get_text())
            m = re.search(r"[:\-]\s*(.+)", same_line)
            if m and len(m.group(1)) > 1:
                candidate = clean(m.group(1))
                if candidate.lower() != title:
                    texts.append(candidate)

            sibling = tag.find_next_sibling(["dd", "span", "p", "div", "td"])
            if sibling:
                txt = clean(sibling.get_text())
                if txt and txt.lower() != title:
                    texts.append(txt)

            parent = tag.parent

            if parent:

                for p in parent.find_all(["li", "p", "span", "div", "dd", "td"]):

                    txt = clean(p.get_text())

                    if txt and txt.lower() != title and heading not in txt.lower():

                        texts.append(txt)

            if texts:
                return "\n".join(dict.fromkeys(texts))

    flat_text = soup.get_text("\n", strip=True)
    m = re.search(
        rf"{re.escape(heading)}\s*[:\-]\s*(.+)",
        flat_text,
        re.IGNORECASE
    )
    if m:
        candidate = clean(m.group(1))
        if 0 < len(candidate) < 300:
            return candidate

    return ""


def get_field(soup, keywords):
    for keyword in keywords:
        value = get_section_text(soup, keyword)
        if value:
            return value
    return ""


# -----------------------------------------------------------------
# Profile photo extraction
# -----------------------------------------------------------------

def extract_profile_photo(soup, doctor_name=""):
    """
    Priority order:
    1. og:image / twitter:image meta tags
    2. <img> whose alt text shares the doctor's name (most reliable
       on this site -- confirmed the profile photo's alt exactly
       matches the <h1> doctor name)
    3. <img> whose class/id/alt/src hints doctor/profile/physician
    4. First reasonably-sized image that isn't an obvious logo/icon
    """

    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        return og["content"]

    twitter = soup.find("meta", attrs={"name": "twitter:image"})
    if twitter and twitter.get("content"):
        return twitter["content"]

    candidates = soup.find_all("img")

    if doctor_name:
        name_words = set(
            w for w in re.sub(r"\bdr\.?\b", "", doctor_name, flags=re.IGNORECASE).lower().split()
            if len(w) > 1
        )

        for img in candidates:
            alt = (img.get("alt") or "").lower()
            alt_words = set(alt.split())
            if name_words and len(alt_words & name_words) >= 2:
                return img.get("src", "")

    keywords = ["doctor", "physician", "profile", "consultant", "dr-", "dr_"]

    for img in candidates:

        attrs_text = " ".join([
            img.get("class", [""])[0] if img.get("class") else "",
            img.get("id", ""),
            img.get("alt", ""),
            img.get("src", "")
        ]).lower()

        if any(k in attrs_text for k in keywords) and "logo" not in attrs_text and "icon" not in attrs_text:
            return img.get("src", "")

    skip_words = ["logo", "icon", "facebook", "twitter", "instagram", "linkedin", "sprite", "placeholder"]

    for img in candidates:

        src = img.get("src", "")

        if not src:
            continue

        src_lower = src.lower()

        if any(w in src_lower for w in skip_words):
            continue

        width = img.get("width")
        height = img.get("height")

        try:
            if width and int(width) < 80:
                continue
            if height and int(height) < 80:
                continue
        except ValueError:
            pass

        return src

    return ""


# -----------------------------------------------------------------
# Publications heuristic
# -----------------------------------------------------------------
# On several profiles (e.g. Dr. Deepak Solanki) there's no separate
# "Publications:" label -- a publications line is embedded as a
# sentence inside the Awards section instead. This pulls it out.

def split_publications_from_awards(awards_text):
    """
    Returns (publications_text, awards_text).

    Note: on this site, text pasted from Word often wraps a single
    sentence across several lines with no punctuation to mark clause
    boundaries, so a "Journal Publications ..." mention buried inside
    the Awards blob can't always be cleanly cut out without risking
    truncating it (or the award text) mid-sentence. When that mention
    is present we duplicate the full flattened text into Publications
    rather than risk mangling either field -- safe, if slightly
    redundant, over losing/breaking real content.
    """

    if not awards_text or "publication" not in awards_text.lower():
        return "", awards_text

    flat = clean(awards_text)

    return flat, awards_text


def scrape_doctor_profile(profile_url):

    response = requests.get(
        profile_url,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    result = {

        "designation": "",
        "department": "",
        "qualification": "",
        "experience": "",
        "languages": "",
        "expertise": "",
        "procedures_performed": "",
        "professional_memberships": "",
        "publications": "",
        "awards": "",
        "consultation_location": "",
        "summary": "",
        "profile_photo": "",
        "hospital_name": "Artemis Hospitals"

    }

    # -------------------------
    # DOCTOR NAME (used for photo matching)
    # -------------------------

    h1 = soup.find("h1")
    doctor_name = clean(h1.get_text()) if h1 else ""

    # -------------------------
    # JSON-LD (photo, summary, department)
    # -------------------------

    result.update(extract_jsonld(soup))

    # -------------------------
    # PROFILE PHOTO
    # -------------------------

    if not result["profile_photo"]:
        result["profile_photo"] = extract_profile_photo(soup, doctor_name)

    text = soup.get_text("\n", strip=True)

    # -------------------------
    # DESIGNATION
    # -------------------------

    result["designation"] = find_text_by_id_suffix(soup, "LabelDepartment")

    if not result["designation"]:

        designation_patterns = [
            r"Senior\s+Consultant.*",
            r"Sr\.\s*Consultant.*",
            r"Associate\s+Consultant.*",
            r"Consultant.*",
            r"Chief\s+Consultant.*",
            r"Professor.*",
            r"Head.*"
        ]

        for pattern in designation_patterns:

            m = re.search(pattern, text, re.IGNORECASE)

            if m:
                value = clean(m.group())
                if "Board of Directors" not in value:
                    result["designation"] = value
                    break

    # -------------------------
    # DEPARTMENT / SPECIALITY
    # -------------------------

    specialty_value = find_text_by_id_suffix(soup, "LabelSpecialtyValue")

    if specialty_value:
        result["department"] = specialty_value

    elif not result["department"]:

        department = get_field(soup, [
            "Speciality",
            "Specialty",
            "Department",
            "Area of Specialization",
            "Specialization",
            "Medical Specialty"
        ])

        if department and len(department) < 100:
            result["department"] = department

    # -------------------------
    # PROFILE CONTENT BLOCK
    # (Qualifications / Experience / Procedures / Clinical Focus /
    #  Memberships / Awards all usually live inside this one block)
    # -------------------------

    content_el = find_element_by_id_suffix(soup, "LabelContent")
    parsed = {}

    if content_el:
        content_text = content_el.get_text("\n", strip=True)
        parsed = parse_profile_content(content_text)

    # -------------------------
    # QUALIFICATION
    # -------------------------

    result["qualification"] = get_from_parsed(parsed, "qualifications", "qualification")

    if not result["qualification"]:

        result["qualification"] = get_field(soup, [
            "Qualifications",
            "Qualification",
            "Education",
            "Academic Qualifications",
            "Educational Qualification"
        ])

    if not result["qualification"]:

        degrees = [
            "MBBS", "MD", "MS", "DM", "MCh", "DNB", "FRCS", "MRCP", "FACP", "PhD"
        ]

        found = []
        full_text = soup.get_text(" ", strip=True)

        for degree in degrees:
            if degree in full_text:
                found.append(degree)

        result["qualification"] = ", ".join(sorted(set(found)))

    # -------------------------
    # EXPERIENCE
    # -------------------------

    result["experience"] = get_from_parsed(parsed, "work experience", "experience", "years of experience")

    if not result["experience"]:

        result["experience"] = get_field(soup, [
            "Years of Experience",
            "Experience",
            "Work Experience",
            "Total Experience",
            "Professional Experience"
        ])

    if not result["experience"]:

        m = re.search(
            r"(\d+\+?\s*years?\s*(of\s+)?(experience)?)",
            text,
            re.IGNORECASE
        )

        if m:
            result["experience"] = clean(m.group(1))

    # -------------------------
    # LANGUAGES
    # -------------------------

    result["languages"] = find_text_by_id_suffix(soup, "LabelLanguagesValue")

    if not result["languages"]:
        result["languages"] = get_from_parsed(parsed, "languages", "languages spoken")

    if not result["languages"]:

        result["languages"] = get_field(soup, [
            "Languages Spoken",
            "Languages Known",
            "Languages",
            "Language"
        ])

    # -------------------------
    # EXPERTISE / CLINICAL FOCUS
    # -------------------------

    result["expertise"] = get_from_parsed(
        parsed, "clinical focus", "areas of expertise", "area of expertise", "expertise"
    )

    if not result["expertise"]:

        result["expertise"] = get_field(soup, [
            "Areas of Expertise",
            "Area of Expertise",
            "Clinical Focus",
            "Areas of Interest",
            "Area of Interest",
            "Special Interest",
            "Key Expertise",
            "Expertise"
        ])

    # -------------------------
    # PROCEDURES PERFORMED
    # -------------------------

    result["procedures_performed"] = get_from_parsed(
        parsed, "procedures performed", "procedures"
    )

    if not result["procedures_performed"]:

        result["procedures_performed"] = get_field(soup, [
            "Procedures Performed",
            "Key Procedures",
            "Surgical Procedures",
            "Procedures"
        ])

    # -------------------------
    # PROFESSIONAL MEMBERSHIPS
    # -------------------------

    result["professional_memberships"] = get_from_parsed(
        parsed, "memberships", "professional memberships", "membership"
    )

    if not result["professional_memberships"]:

        result["professional_memberships"] = get_field(soup, [
            "Professional Memberships",
            "Memberships",
            "Membership",
            "Affiliations",
            "Professional Affiliations"
        ])

    # -------------------------
    # AWARDS
    # -------------------------

    result["awards"] = get_from_parsed(
        parsed, "honors and awards", "honours and awards", "awards"
    )

    if not result["awards"]:

        result["awards"] = get_field(soup, [
            "Awards",
            "Awards & Recognition",
            "Awards and Recognition",
            "Achievements",
            "Honours",
            "Honors"
        ])

    # -------------------------
    # PUBLICATIONS
    # -------------------------

    result["publications"] = get_from_parsed(parsed, "publications", "research publications")

    if not result["publications"]:

        result["publications"] = get_field(soup, [
            "Publications",
            "Publication",
            "Research Publications",
            "Papers Published"
        ])

    if not result["publications"]:
        # Some profiles bury a publications mention inside the Awards text
        pub_text, _ = split_publications_from_awards(result["awards"])
        if pub_text:
            result["publications"] = pub_text

    # -------------------------
    # CONSULTATION LOCATION
    # -------------------------

    result["consultation_location"] = find_text_by_id_suffix(soup, "LabelLocationValue")

    if not result["consultation_location"]:

        result["consultation_location"] = get_field(soup, [
            "Consultation Location",
            "Consultation Timings",
            "Available At",
            "Hospital Location",
            "Location"
        ])

    # -------------------------
    # SUMMARY
    # -------------------------

    if not result["summary"]:

        paragraphs = soup.find_all("p")
        longest = ""

        for p in paragraphs:
            txt = clean(p.get_text())
            if len(txt) > len(longest):
                longest = txt

        result["summary"] = longest

    # -------------------------
    # CLEAN EMPTY VALUES
    # -------------------------

    for key, value in result.items():
        if value is None:
            result[key] = ""

    print("\n==========================")
    print(profile_url)
    print(result)
    print("==========================\n")

    return result