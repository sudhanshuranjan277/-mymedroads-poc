from dataclasses import dataclass


@dataclass
class Doctor:


    doctor_id: int = 0

    hospital_id: int = 0

    hospital_name: str = ""


    doctor_name: str = ""

    specialty: str = ""

    profile_url: str = ""

    appointment_url: str = ""


    designation: str = ""

    department: str = ""


    qualification: str = ""

    experience: str = ""

    expertise: str = ""


    procedures_performed: str = ""


    professional_memberships: str = ""

    languages: str = ""


    publications: str = ""

    awards: str = ""


    consultation_location: str = ""


    summary: str = ""


    profile_photo: str = ""



    def to_dict(self):

        return {

            "doctor_id":
                self.doctor_id,

            "hospital_id":
                self.hospital_id,

            "hospital_name":
                self.hospital_name,

            "doctor_name":
                self.doctor_name,

            "specialty":
                self.specialty,

            "profile_url":
                self.profile_url,

            "appointment_url":
                self.appointment_url,

            "designation":
                self.designation,

            "department":
                self.department,

            "qualification":
                self.qualification,

            "experience":
                self.experience,

            "expertise":
                self.expertise,

            "procedures_performed":
                self.procedures_performed,

            "professional_memberships":
                self.professional_memberships,

            "languages":
                self.languages,

            "publications":
                self.publications,

            "awards":
                self.awards,

            "consultation_location":
                self.consultation_location,

            "summary":
                self.summary,

            "profile_photo":
                self.profile_photo
        }