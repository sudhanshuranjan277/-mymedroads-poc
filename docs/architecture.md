# myMedroads POC - System Architecture

## 1. System Overview

The solution follows a modular ETL (Extract → Transform → Load) architecture.

The scraper collects publicly available information from Artemis Hospitals, processes and validates the extracted data, and generates import-ready datasets (JSON, CSV, SQL) for the myMedroads platform.

---

# 2. High-Level Architecture

```text
                         myMedroads Platform
                   (Target Data Requirements)
                                │
                                │
                                ▼
                    Study Required Data Fields
                                │
                                ▼
                    Artemis Hospital Website
                                │
                                ▼
                     Configuration Layer
                (URLs, Selectors, Settings)
                                │
                                ▼
                      Web Scraper Engine
         (Requests, Sessions, Retry, Timeout)
                                │
                                ▼
                        HTML Downloader
                                │
                                ▼
                         HTML Parser
                    (BeautifulSoup / lxml)
                                │
                                ▼
                     Information Extractor
            ┌───────────────────────────────────┐
            │                                   │
            ▼                                   ▼
     Hospital Information               Doctor Information
            │                                   │
            └──────────────┬────────────────────┘
                           ▼
                     Data Cleaning Layer
             • Remove duplicates
             • Normalize text
             • Handle null values
             • Standardize formatting
                           │
                           ▼
                    Data Validation Layer
             • Mandatory field validation
             • Image validation
             • Record count validation
             • Duplicate validation
             • Relationship validation
                           │
                           ▼
                       Data Models
                 Hospital <──► Doctor
                           │
                           ▼
                     Export Layer
         JSON │ CSV │ SQL │ Future Database
                           │
                           ▼
                   Validation Report
                   Technical Document
                        README
```

---

# 3. Layer Architecture

## Layer 1 – Configuration Layer

Purpose

Store all configurable values separately from the source code.

Responsibilities

• Base URL
• Hospital URL
• Doctor Listing URL
• CSS Selectors
• XPath (if required)
• Timeout
• Retry Count

Files

config/
    artemis.json

Future

config/
    apollo.json
    fortis.json
    max.json

No scraper code changes required.

---

## Layer 2 – Scraper Layer

Purpose

Download webpages.

Responsibilities

• HTTP Requests
• Session Management
• Timeout Handling
• Retry Logic
• Logging
• Rate Limiting

Output

Raw HTML

---

## Layer 3 – Parser Layer

Purpose

Convert HTML into structured information.

Libraries

BeautifulSoup

lxml

Responsibilities

Locate HTML elements

Extract text

Extract images

Extract links

Output

Python Dictionary

---

## Layer 4 – Extraction Layer

Hospital Fields

Hospital Name

Address

Contact

Email

Website

Overview

Awards

Infrastructure

Centres of Excellence

Images

Accreditations

Doctor Fields

Doctor Name

Designation

Department

Speciality

Qualification

Experience

Procedures

Languages

Awards

Profile Summary

Image

Hospital Name

Output

Structured Raw Data

---

## Layer 5 – Cleaning Layer

Responsibilities

Remove duplicate doctors

Remove duplicate hospitals

Trim extra spaces

Normalize phone numbers

Normalize URLs

Convert missing values to null

Clean unwanted characters

Output

Clean Dataset

---

## Layer 6 – Validation Layer

Responsibilities

Mandatory field validation

Missing value detection

Duplicate detection

Broken image detection

Hospital-Doctor relationship validation

Record count verification

Output

Validated Dataset

---

## Layer 7 – Data Model Layer

Hospital

↓

Doctor

Relationship

One Hospital

↓

Many Doctors

Database Model

Hospital

hospital_id

name

address

website

...

Doctor

doctor_id

hospital_id (Foreign Key)

name

qualification

experience

...

---

## Layer 8 – Export Layer

Generate

hospital.json

doctor.json

hospital.csv

doctor.csv

database.sql

Future

REST API

MongoDB

PostgreSQL

MySQL

---

## Layer 9 – Reporting Layer

Generate

Validation Report

Technical Documentation

README

Execution Logs

---

# 4. Data Flow

```text
Website
   │
   ▼
Download HTML
   │
   ▼
Parse HTML
   │
   ▼
Extract Information
   │
   ▼
Clean Data
   │
   ▼
Validate Data
   │
   ▼
Build Data Models
   │
   ▼
Generate JSON
CSV
SQL
   │
   ▼
Reports
```

---

# 5. Folder Mapping

```text
config/
    Configuration files

scraper/
    Download webpages

models/
    Hospital & Doctor models

validator/
    Validation logic

exporter/
    JSON / CSV / SQL generation

output/
    Generated datasets

logs/
    Execution logs

docs/
    Architecture
    Technical Documentation
    Validation Report

main.py
    Entry point
```

---

# 6. Scalability

The architecture is configuration-driven.

To add another hospital:

Create

config/apollo.json

OR

config/fortis.json

Update selectors only.

No scraper logic changes are required.

This makes the solution reusable for multiple hospitals and aligns with the assignment's scalability requirement.

---

# 7. Future Improvements

• Multi-threaded scraping

• Asynchronous requests

• Database integration

• Scheduler (Cron)

• Docker support

• REST API

• Monitoring Dashboard

• ETL Pipeline

• Unit Testing

• CI/CD Integration


# 8. System Workflow

The myMedroads POC follows an ETL (Extract, Transform, Load) pipeline to collect structured hospital and doctor information from publicly available sources and generate import-ready datasets.

---

## Step 1 – Study the Target Platform

The process begins by analyzing the myMedroads website to understand the required data model.

This includes identifying:

- Hospital fields
- Doctor fields
- Mandatory attributes
- Optional attributes
- Images
- Relationships between hospitals and doctors

This step defines the target schema that the scraper must populate.

↓

---

## Step 2 – Load Configuration

The application reads the hospital-specific configuration file.

Example:

```
config/artemis.json
```

The configuration contains:

- Base URL
- Hospital URL
- Doctor Listing URL
- CSS Selectors
- XPath (if required)
- Retry Settings
- Timeout Settings

Keeping these values outside the code allows the scraper to support multiple hospitals with minimal modifications.

↓

---

## Step 3 – Download Web Pages

The Scraper Engine sends HTTP requests to the Artemis Hospital website.

Responsibilities include:

- Creating HTTP sessions
- Sending requests
- Managing headers
- Timeout handling
- Retry mechanism
- Error logging

Output:

```
Raw HTML Pages
```

↓

---

## Step 4 – Parse HTML

The downloaded HTML is processed using BeautifulSoup.

The parser locates HTML elements such as:

- Hospital Name
- Address
- Doctor Cards
- Qualification
- Experience
- Images
- Contact Details

Output:

```
Structured Python Objects
```

↓

---

## Step 5 – Extract Information

The parser extracts all required information.

Hospital Information

- Name
- Address
- Contact Details
- Website
- Overview
- Accreditations
- Awards
- Centres of Excellence
- Infrastructure
- Emergency Services
- Images

Doctor Information

- Name
- Designation
- Department
- Speciality
- Qualification
- Experience
- Procedures
- Languages
- Publications
- Awards
- Summary
- Profile Image
- Consultation Location

Output:

```
Raw Dataset
```

↓

---

## Step 6 – Data Cleaning

The extracted data is cleaned before storage.

Cleaning operations include:

- Remove duplicate records
- Trim whitespace
- Normalize text
- Convert missing values to NULL
- Standardize URLs
- Normalize phone numbers
- Remove invalid characters

Output:

```
Clean Dataset
```

↓

---

## Step 7 – Data Validation

The cleaned dataset is validated to ensure quality.

Validation checks include:

- Mandatory field validation
- Missing value detection
- Duplicate detection
- Image URL validation
- Record count verification
- Hospital–Doctor relationship validation

Any validation issues are logged for review.

Output:

```
Validated Dataset
```

↓

---

## Step 8 – Data Modeling

The validated data is converted into normalized data models.

Hospital Model

```
Hospital
│
├── hospital_id
├── name
├── address
├── website
└── ...
```

Doctor Model

```
Doctor
│
├── doctor_id
├── hospital_id
├── name
├── qualification
└── ...
```

Each doctor references the corresponding hospital through the `hospital_id`, maintaining referential integrity.

↓

---

## Step 9 – Export Data

The Export Module converts the validated dataset into multiple import-ready formats.

Generated Files

- hospital.json
- doctors.json
- hospital.csv
- doctors.csv
- database.sql

These files can be directly consumed by the myMedroads technology team.

↓

---

## Step 10 – Generate Reports

After successful execution, the system generates:

- Validation Report
- Execution Logs
- Technical Documentation
- README

The validation report summarizes:

- Total hospitals extracted
- Total doctors extracted
- Missing values
- Duplicate records
- Validation statistics
- Execution time

---

# Complete Workflow Diagram

```text
                 Study myMedroads Website
                           │
                           ▼
                 Load Configuration File
                           │
                           ▼
                  Download Web Pages
                           │
                           ▼
                     Parse HTML Pages
                           │
                           ▼
                 Extract Hospital Data
                           │
                 Extract Doctor Data
                           │
                           ▼
                    Clean Extracted Data
                           │
                           ▼
                     Validate Dataset
                           │
                           ▼
                  Build Data Models
                           │
                           ▼
            Export JSON / CSV / SQL Files
                           │
                           ▼
         Generate Logs & Validation Reports
                           │
                           ▼
          Ready for myMedroads Database Import
```

## Advantages of the Architecture

- Modular and maintainable
- Configuration-driven for multiple hospitals
- Separation of concerns (scraping, parsing, validation, export)
- ETL-based workflow suitable for production systems
- Easily extensible to Apollo, Fortis, Max, Manipal, and other hospital websites
- Generates import-ready data with minimal manual intervention