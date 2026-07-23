# MyMedRoads POC - Hospital & Doctor Data Scraper

## Project Overview

MyMedRoads POC is a web scraping pipeline developed to extract structured hospital and doctor information from Artemis Hospitals website.

The system collects:

- Hospital details
- Doctor listing information
- Individual doctor profile details

The extracted data is validated and exported into multiple formats such as CSV, JSON, and SQL.

---

# Features

## Hospital Data Extraction

Extracts:

- Hospital Name
- Location
- Address
- Contact Details
- Website
- Overview
- Centres of Excellence
- Emergency Services
- International Patient Services
- Hospital Images
- Awards and Accreditations (where available)


## Doctor Data Extraction

Extracts:

- Doctor Name
- Specialty
- Department
- Designation
- Profile URL
- Appointment URL
- Qualification
- Experience
- Languages Spoken
- Areas of Expertise
- Procedures Performed
- Professional Memberships
- Publications
- Awards
- Consultation Location
- Doctor Profile Summary
- Profile Photograph


---

# Tech Stack

## Programming Language

- Python 3.x


## Libraries

- Requests
- BeautifulSoup4
- JSON
- Regular Expressions
- CSV


---

# Project Architecture
MyMedRoads-POC

|
|-- scraper
| |
| |-- hospital_scraper.py
| |-- doctor_scraper.py
| |-- doctor_profile_scraper.py
| |-- parser.py
| |-- utils.py
|
|-- exporter
| |
| |-- csv_export.py
| |-- json_export.py
| |-- sql_export.py
|
|-- models
| |
| |-- hospital.py
| |-- doctor.py
|
|-- docs
| |
| |-- architecture.md
| |-- DATA_SCHEMA.md
| |-- TECHNICAL_DOCUMENTATION.md
| |-- VALIDATION_REPORT.md
|
|-- output
| |
| |-- hospital.csv
| |-- doctors.csv
| |-- data.json
| |-- doctors.sql
|
|-- main.py
|-- validation.py
|-- requirements.txt


---

# Installation

Clone the repository:

```bash
git clone https://github.com/sudhanshuranjan277/-mymedroads-poc.git

cd mymedroads-poc

pip install -r requirements.txt

#How To Run
python main.py

#The pipeline performs:

Hospital information scraping
Doctor listing extraction
Doctor profile scraping
Data validation
CSV export
JSON export
SQL export
Validation

#The validation module checks:

Total doctor count
Duplicate doctor names
Missing doctor names
Missing profile URLs
Required doctor fields
Required hospital fields

#Data Handling

The scraper maintains a structured schema for hospital and doctor records.

Missing fields are handled gracefully when information is unavailable on the source website.

#Future Improvements

Possible improvements:

Better handling of dynamic content
Additional hospital fields extraction
Automated scheduling
Database integration
API based data delivery

#Author

Sudhanshu Ranjan

```powershell
git status
