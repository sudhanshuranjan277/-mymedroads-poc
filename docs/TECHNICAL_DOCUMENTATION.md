# Technical Documentation

# MyMedRoads POC - Hospital & Doctor Data Extraction Pipeline


## 1. Introduction

MyMedRoads POC is a Python-based healthcare data extraction pipeline designed to collect structured hospital and doctor information from healthcare websites.

The objective of this project is to automate the extraction of healthcare directory information and transform unstructured website content into clean, normalized, and import-ready datasets.

The pipeline performs:

- Web data extraction
- HTML parsing
- Data cleaning
- Data normalization
- Data validation
- Multi-format export


The final processed data is generated in:

- CSV format
- JSON format
- SQL format


---

# 2. Project Objective

The primary objectives of this POC are:

- Extract hospital-level information
- Extract detailed doctor profile information
- Maintain a consistent data schema
- Validate extracted records
- Generate datasets suitable for healthcare platforms like MyMedRoads


---

# 3. System Architecture


```
                    Hospital Website
                           |
                           |
                  Web Scraping Layer
                           |
        ---------------------------------------
        |                                     |
 Hospital Scraper                    Doctor Listing Scraper
        |                                     |
        |                                     |
        |                          Doctor Profile Scraper
        |                                     |
        ---------------------------------------
                           |
                           |
                  Data Processing Layer
                           |
                           |
                  Validation Layer
                           |
                           |
                   Export Layer
             -----------------------------
             |             |             |
            CSV           JSON          SQL

```


The overall workflow follows an ETL architecture:

```
Extract  →  Transform  →  Validate  →  Export
```


---

# 4. Technology Stack


## Programming Language

- Python 3.x


## Libraries Used


### Requests

Used for:

- Sending HTTP requests
- Fetching webpage content
- Handling communication with source websites


### BeautifulSoup4

Used for:

- HTML parsing
- Extracting structured information
- Navigating webpage elements


### Pandas

Used for:

- Data processing
- Dataset validation
- CSV generation


### Regular Expressions (Regex)

Used for:

- Pattern matching
- Experience extraction
- Text cleaning


### Dataclasses

Used for:

- Maintaining structured data models
- Creating consistent object schemas


---

# 5. Project Structure


```
mymedroads-poc

│
├── main.py
├── validation.py
├── requirements.txt
│
├── config
│
├── scraper
│   ├── hospital_scraper.py
│   ├── doctor_scraper.py
│   ├── doctor_profile_scraper.py
│   ├── parser.py
│   └── utils.py
│
├── models
│   ├── hospital.py
│   └── doctor.py
│
├── exporter
│   ├── csv_export.py
│   ├── json_export.py
│   └── sql_export.py
│
├── docs
│
└── output

```


---

# 6. Scraping Modules


## 6.1 Hospital Scraper


File:

```
scraper/hospital_scraper.py
```


Responsibilities:

- Extract hospital details
- Extract location information
- Extract address
- Extract contact details
- Extract website information
- Extract hospital overview
- Extract accreditations
- Extract infrastructure details
- Extract emergency services
- Extract international patient services
- Extract hospital images
- Extract awards


Output:

Structured hospital data object.


---

## 6.2 Doctor Listing Scraper


File:

```
scraper/doctor_scraper.py
```


Responsibilities:

- Extract doctor listing pages
- Collect doctor names
- Collect specialties
- Collect profile URLs
- Collect available appointment links


Output:

Basic doctor information list.


---

## 6.3 Doctor Profile Scraper


File:

```
scraper/doctor_profile_scraper.py
```


Responsibilities:

Extract detailed doctor information:


- Doctor Name
- Designation
- Department
- Specialty
- Qualification
- Years of Experience
- Areas of Expertise
- Procedures Performed
- Professional Memberships
- Languages Spoken
- Publications
- Awards
- Consultation Location
- Profile Summary
- Profile Photograph


Each doctor profile is processed independently to avoid failure of the complete pipeline.


---

# 7. Data Processing and Cleaning


Before exporting, extracted information is cleaned and normalized.


Cleaning operations include:


- Removing HTML entities
- Removing unwanted whitespace
- Removing empty formatting characters
- Standardizing text format
- Handling missing values
- Maintaining consistent field structure


Example:


Before:

```
M.B.B.S.&nbsp; M.D
```


After:

```
M.B.B.S. M.D
```


---

# 8. Data Models


The project maintains structured schemas:


## Doctor Model

Contains:

- Doctor ID
- Hospital ID
- Doctor Name
- Specialty
- Qualification
- Experience
- Expertise
- Procedures
- Memberships
- Publications
- Awards
- Profile Information


## Hospital Model

Contains:

- Hospital ID
- Hospital Name
- Location
- Address
- Contact Details
- Website
- Overview
- Services
- Infrastructure
- Images


---

# 9. Validation System


File:

```
validation.py
```


The validation module ensures extracted data quality before export.


## Doctor Validation


Performed checks:


```
Total Doctors Extracted : 163

Duplicate Names         : 0

Missing Doctor Names    : 0

Missing Profile URLs    : 0
```


Field validation:


```
doctor_name        PASS
designation        PASS
department         PASS
qualification      PASS
summary            PASS
profile_photo      PASS
```


---

## Hospital Validation


Checks:


- Hospital Name
- Address
- Website
- Required information availability


---

# 10. Handling Missing Data


The pipeline follows source-data availability rules.


Not every doctor profile contains all optional information.

Fields like:

- Experience
- Publications
- Awards
- Memberships
- Languages


may not be available for every profile.


In such cases:

- Empty values are preserved
- No incorrect assumptions are generated
- Data accuracy is maintained


---

# 11. Export System


## CSV Export


File:

```
exporter/csv_export.py
```


Generated files:


```
hospital.csv

doctors.csv
```



---

## JSON Export


File:

```
exporter/json_export.py
```


Generated files:


```
data.json

hospital.json
```



---

## SQL Export


File:

```
exporter/sql_export.py
```


Generated file:


```
doctors.sql
```


The SQL output can be directly used for database ingestion.


---

# 12. Execution Flow


Complete pipeline execution:


```
main.py

    |
    ↓

Extract Hospital Data

    |
    ↓

Extract Doctor Listing

    |
    ↓

Extract Doctor Profiles

    |
    ↓

Clean and Normalize Data

    |
    ↓

Validate Records

    |
    ↓

Generate CSV / JSON / SQL Files

```


---

# 13. Error Handling


The scraper handles:


- Failed HTTP requests
- Missing webpage elements
- Empty fields
- Incomplete doctor profiles
- Parsing failures


If one doctor profile fails, the remaining profiles continue processing.


---

# 14. Generated Output


Final output directory:


```
output/

├── hospital.csv
├── doctors.csv
├── hospital.json
├── data.json
├── doctors.sql
└── validation_report.txt

```


---

# 15. Limitations


Current limitations:


- Data availability depends on the source website
- Some optional doctor fields may not exist
- Website structure changes may require scraper updates
- Dynamic content handling can be improved further


---

# 16. Future Improvements


Possible enhancements:


- Database integration
- REST API development
- Scheduled automated scraping
- Support for multiple hospitals
- Cloud deployment
- Incremental data updates
- Monitoring dashboard


---

# 17. Conclusion


The MyMedRoads POC successfully implements a complete healthcare data extraction pipeline.

The system is capable of:

- Extracting hospital information
- Extracting doctor profiles
- Cleaning and validating healthcare data
- Generating structured datasets


The modular design allows future expansion into a production-ready healthcare directory platform.
