# myMedroads POC - Data Schema

## Overview

This document defines the data schema used throughout the project.

The schema is designed based on:

- Target Platform: myMedroads
- Source Website: Artemis Hospitals

The objective is to generate a normalized dataset that can be directly imported into the myMedroads platform with minimal manual intervention.

---

# Entity Relationship Diagram (ERD)

```text
                 Hospital
             -----------------
             hospital_id (PK)
                    │
                    │
             One Hospital
                    │
                    ▼
              Multiple Doctors
                    │
                    │
          hospital_id (FK)
```

Relationship

```
One Hospital
      │
      ├──────── Doctor 1
      ├──────── Doctor 2
      ├──────── Doctor 3
      └──────── Doctor N
```

---

# Hospital Schema

| Field Name | Data Type | Required | Nullable | Source |
|------------|----------|----------|----------|--------|
| hospital_id | Integer | Yes | No | Generated |
| hospital_name | String | Yes | No | Artemis |
| location | String | Yes | No | Artemis |
| address | String | Yes | No | Artemis |
| city | String | Yes | No | Artemis |
| state | String | Yes | No | Artemis |
| country | String | Yes | No | Artemis |
| phone | String | Yes | Yes | Artemis |
| email | String | No | Yes | Artemis |
| website | String | Yes | No | Artemis |
| overview | Text | Yes | Yes | Artemis |
| accreditations | List[String] | No | Yes | Artemis |
| number_of_beds | Integer | No | Yes | Artemis |
| centres_of_excellence | List[String] | No | Yes | Artemis |
| infrastructure | Text | No | Yes | Artemis |
| emergency_services | Boolean | No | Yes | Artemis |
| international_patient_services | Boolean | No | Yes | Artemis |
| awards | List[String] | No | Yes | Artemis |
| image_urls | List[String] | No | Yes | Artemis |
| created_at | DateTime | Yes | No | System |
| updated_at | DateTime | Yes | No | System |

---

# Doctor Schema

| Field Name | Data Type | Required | Nullable | Source |
|------------|----------|----------|----------|--------|
| doctor_id | Integer | Yes | No | Generated |
| hospital_id | Integer | Yes | No | Generated |
| doctor_name | String | Yes | No | Artemis |
| designation | String | Yes | Yes | Artemis |
| department | String | Yes | Yes | Artemis |
| speciality | String | Yes | Yes | Artemis |
| qualification | String | Yes | Yes | Artemis |
| experience_years | Integer | Yes | Yes | Artemis |
| areas_of_expertise | List[String] | No | Yes | Artemis |
| procedures | List[String] | No | Yes | Artemis |
| professional_memberships | List[String] | No | Yes | Artemis |
| languages_spoken | List[String] | No | Yes | Artemis |
| publications | List[String] | No | Yes | Artemis |
| awards | List[String] | No | Yes | Artemis |
| profile_summary | Text | No | Yes | Artemis |
| consultation_location | String | No | Yes | Artemis |
| profile_photo | String | No | Yes | Artemis |
| profile_url | String | Yes | No | Artemis |
| created_at | DateTime | Yes | No | System |
| updated_at | DateTime | Yes | No | System |

---

# Relationship Rules

Every hospital has a unique identifier.

```
hospital_id
```

Every doctor stores the corresponding hospital identifier.

```
doctor.hospital_id
```

This creates a One-to-Many relationship.

Example

```
Hospital

hospital_id = 1

↓

Doctors

hospital_id = 1

hospital_id = 1

hospital_id = 1
```

---

# Mandatory Fields

## Hospital

- hospital_name
- address
- website
- hospital_id

## Doctor

- doctor_name
- qualification
- department
- speciality
- experience_years
- profile_url
- hospital_id

---

# Null Value Handling

If a value is unavailable on the source website, it will be stored as:

```
NULL
```

Examples

```
publications = NULL

languages_spoken = NULL

awards = NULL
```

---

# Naming Convention

The project follows snake_case naming.

Examples

```
hospital_name

doctor_name

profile_photo

experience_years

consultation_location
```

---

# Data Validation Rules

The validator performs the following checks:

✓ Mandatory field validation

✓ Duplicate hospital detection

✓ Duplicate doctor detection

✓ Missing value detection

✓ Image URL validation

✓ Website URL validation

✓ Hospital–Doctor relationship validation

✓ Record count verification

---

# Output Files

The schema is exported into the following formats:

```
output/

hospital.json

doctors.json

hospital.csv

doctors.csv

database.sql
```

These files are designed to be directly consumable by the myMedroads technology team.

---

# Future Scalability

The schema is generic and reusable.

It can support additional hospitals by updating the configuration file only.

Examples

```
config/

artemis.json

apollo.json

fortis.json

max.json

manipal.json
```

No changes are required to the core schema or export logic.