from dataclasses import dataclass, field
from typing import List


@dataclass
class Hospital:

    hospital_id: int = 0

    hospital_name: str = ""

    location: str = ""

    address: str = ""

    contact_details: str = ""

    website: str = ""

    overview: str = ""

    accreditations: str = ""

    number_of_beds: str = ""

    centres_of_excellence: str = ""

    infrastructure: str = ""

    emergency_services: str = ""

    international_patient_services: str = ""

    images: str = ""

    awards: str = ""


    def to_dict(self):

        return {

            "hospital_id":
                self.hospital_id,

            "hospital_name":
                self.hospital_name,

            "location":
                self.location,

            "address":
                self.address,

            "contact_details":
                self.contact_details,

            "website":
                self.website,

            "overview":
                self.overview,

            "accreditations":
                self.accreditations,

            "number_of_beds":
                self.number_of_beds,

            "centres_of_excellence":
                self.centres_of_excellence,

            "infrastructure":
                self.infrastructure,

            "emergency_services":
                self.emergency_services,

            "international_patient_services":
                self.international_patient_services,

            "images":
                self.images,

            "awards":
                self.awards
        }