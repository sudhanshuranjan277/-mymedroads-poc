# Technical Documentation

## Project Name

MyMedRoads POC - Hospital & Doctor Data Scraper


# 1. Introduction

MyMedRoads POC is a Python-based web scraping system designed to extract structured healthcare information from hospital websites.

The system collects hospital-level information and detailed doctor profiles, processes the extracted data, validates the records, and exports the final dataset into CSV, JSON, and SQL formats.


---

# 2. System Architecture

The project follows a modular architecture.

            Website
               |
               |
        Web Scraping Layer
               |
    -------------------------
    |                       |

Hospital Scraper Doctor Scraper
|
|
Doctor Profile Scraper
|
|
Data Processing
|
|
Validation Layer
|
|
Export Layer
-------------------------
| | |
CSV JSON SQL



---

# 3. Technology Stack

## Programming Language

- Python 3.x


## Libraries Used

### Requests

Used for sending HTTP requests and fetching webpage content.


### BeautifulSoup4

Used for parsing HTML documents and extracting required information.


### Regular Expressions (Regex)

Used for pattern-based extraction such as:

- Experience years
- Cleaning text fields


### CSV / JSON

Used for exporting structured data.


---

# 4. Project Modules


## 4.1 Hospital Scraper

File:


scraper/hospital_scraper.py


Responsibilities:

- Extract hospital information
- Parse hospital overview
- Extract contact details
- Extract centres of excellence
- Extract emergency services
- Extract images


Output:

Hospital structured object.


---

## 4.2 Doctor Listing Scraper

File:


scraper/doctor_scraper.py


Responsibilities:

- Extract doctor listing page data
- Collect doctor names
- Collect specialties
- Collect profile URLs
- Collect appointment URLs


Output:

List of doctors with basic information.


---

## 4.3 Doctor Profile Scraper

File:


scraper/doctor_profile_scraper.py


Responsibilities:

Extract detailed doctor information:

- Designation
- Department
- Qualification
- Experience
- Languages
- Expertise
- Professional memberships
- Publications
- Awards
- Consultation location
- Profile summary
- Doctor image


Each doctor profile is processed individually.


---

# 5. Data Processing

Before exporting, extracted information is cleaned.

Cleaning operations include:

- Removing unwanted HTML characters
- Removing markdown symbols
- Removing extra spaces
- Normalizing text format


Example:

Before:


||
|


After cleaning:


Empty string



---

# 6. Validation System

File:


validation.py


The validation module performs:


## Doctor Validation

Checks:

- Total doctor count
- Duplicate doctor names
- Missing doctor names
- Missing profile URLs
- Required fields availability


## Hospital Validation

Checks:

- Hospital name
- Address
- Website


Validation is performed before exporting data.


---

# 7. Export System


## CSV Export

File:


exporter/csv_export.py


Generates:


hospital.csv
doctors.csv



## JSON Export

File:


exporter/json_export.py


Generates:


data.json



## SQL Export

File:


exporter/sql_export.py


Generates:


doctors.sql



---

# 8. Execution Flow


The complete execution pipeline:


main.py

|
|

Scrape Hospital Data

|
|

Scrape Doctor Listing

|
|

Scrape Doctor Profiles

|
|

Validate Extracted Data

|
|

Export Final Dataset



---

# 9. Error Handling

The scraper handles:

- Failed profile requests
- Missing fields
- Empty values
- Incomplete information


If a doctor profile fails, the pipeline continues processing remaining doctors.


---

# 10. Output Schema

The generated doctor dataset contains:

- Doctor ID
- Hospital ID
- Doctor Name
- Specialty
- Profile URL
- Appointment URL
- Designation
- Department
- Qualification
- Experience
- Languages
- Expertise
- Procedures
- Memberships
- Publications
- Awards
- Consultation Location
- Summary
- Profile Photo


Hospital dataset contains:

- Hospital ID
- Hospital Name
- Location
- Address
- Contact Details
- Website
- Overview
- Services
- Images


---

# 11. Future Improvements

Possible improvements:

- Database integration
- API layer development
- Automated scheduled scraping
- Support for multiple hospitals
- Better dynamic page handling
- Cloud deployment


---

# Conclusion

The MyMedRoads POC successfully implements a complete healthcare data extraction pipeline.

The system can scrape, validate, and export structured hospital and doctor information.