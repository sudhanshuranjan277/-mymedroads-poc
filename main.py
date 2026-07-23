from scraper.hospital_scraper import scrape_hospital
from scraper.doctor_scraper import scrape_doctors
from scraper.doctor_profile_scraper import scrape_doctor_profile

from exporter.csv_export import export_to_csv
from exporter.json_export import save_json
from exporter.sql_export import save_doctors_sql

from validation import validate


def main():

    print("========== MyMedRoads POC ==========\n")


    # ==============================
    # Hospital Scraping
    # ==============================

    print("Scraping hospital information...\n")

    hospital_data = scrape_hospital()

    print("✔ Hospital data extracted")


    # ==============================
    # Doctor Listing Scraping
    # ==============================

    print("\nScraping doctor listing...\n")

    doctors_data = scrape_doctors()

    print(
        f"✔ Total doctors found: {len(doctors_data)}"
    )


    # ==============================
    # Doctor Profile Scraping
    # ==============================

    print("\nScraping doctor profiles...\n")


    success = 0
    failed = 0
    failed_doctors = []


    for doctor in doctors_data:

        try:

            profile_data = scrape_doctor_profile(
                doctor["profile_url"]
            )

            doctor.update(profile_data)

            success += 1

            print(
                f"✔ {doctor['doctor_name']}"
            )


        except Exception as e:

            failed += 1

            failed_doctors.append(
                doctor.get(
                    "doctor_name",
                    "Unknown"
                )
            )

            print(
                f"❌ Failed: {doctor.get('doctor_name','Unknown')} -> {e}"
            )


    # ==============================
    # Doctor Summary
    # ==============================

    print("\nDoctor Profile Summary")
    print("----------------------")

    print(
        f"Successful : {success}"
    )

    print(
        f"Failed     : {failed}"
    )


    if failed_doctors:

        print("\nFailed Doctors:")

        for doctor in failed_doctors:

            print(
                "-",
                doctor
            )


    # ==============================
    # Validation
    # ==============================

    print("\nRunning validation...\n")


    validate(
        hospital_data,
        doctors_data
    )


    # ==============================
    # Export CSV
    # ==============================

    print("\nExporting CSV...\n")


    export_to_csv(
        hospital_data,
        doctors_data
    )


    # ==============================
    # Export JSON
    # ==============================

    print("\nExporting JSON...\n")


    save_json(
        {
            "hospital": hospital_data,
            "doctors": doctors_data
        },
        "data.json"
    )


    # ==============================
    # Export SQL
    # ==============================

    print("\nExporting SQL...\n")


    save_doctors_sql(
        doctors_data
    )


    print("\n================================")
    print("✅ All files exported successfully")
    print("================================")



if __name__ == "__main__":

    main()