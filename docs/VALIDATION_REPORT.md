# Validation Report

## Project

MyMedRoads POC - Hospital & Doctor Data Scraper


## Overview

This document describes the validation performed on the extracted hospital and doctor data.

The validation ensures:

- Required fields are available
- Duplicate records are identified
- Profile URLs are present
- Hospital information is complete


---

# Doctor Data Validation


## Total Doctors Extracted
164

## Duplicate Doctor Check
Duplicate Names: 0

## Status:



## Mandatory Field Validation

| Field | Status |
|---|---|
| Doctor Name | PASS |
| Specialty | PASS |
| Profile URL | PASS |
| Designation | PASS |
| Department | PASS |
| Qualification | PASS |
| Experience | PASS (where available) |


---

# Hospital Data Validation


## Hospital Information

| Field | Status |
|---|---|
| Hospital Name | PASS |
| Address | PASS |
| Website | PASS |
| Location | PASS |
| Contact Details | PASS |
| Overview | PASS |


---

# Optional Fields

Some fields may remain empty because information was not available on the source website.

Examples:

| Field | Status |
|---|---|
| Accreditations | Not Available |
| Number of Beds | Not Available |
| Infrastructure | Not Available |
| Awards | Not Available |
| Procedures Performed | Available where provided |


---

# Data Quality Summary
DOCTOR VALIDATION

Total Doctors : 164
Duplicate Names : 0
Missing Names : 0
Missing Profile URL : 0

HOSPITAL VALIDATION

Hospital Name : PASS
Address : PASS
Website : PASS

Validation Completed Successfully



---

# Validation Method

The validation module checks:

1. Total extracted doctor records
2. Duplicate doctor names
3. Missing mandatory fields
4. Hospital required fields
5. Data consistency before export


---

# Conclusion

The extracted dataset successfully passed validation checks.

The final output is ready for export in:

- CSV format
- JSON format
- SQL format



