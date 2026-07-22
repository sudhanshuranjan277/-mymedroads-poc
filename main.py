from scraper.hospital_scraper import scrape_hospital
from exporter.csv_export import export_to_csv
from exporter.json_export import save_json


def main():

    print("========== Hospital Scraper Test ==========\n")


    # Scrape hospital only
    hospital_data = scrape_hospital()


    print("\nHospital Data Extracted:")
    print(hospital_data)


    # Export hospital CSV
    export_to_csv(
        hospital_data,
        []
    )


    # Export JSON
    save_json(
        {
            "hospital": hospital_data
        },
        "hospital_data.json"
    )


    print("\n✅ Hospital export completed.")
    print("===========================================")



if __name__ == "__main__":
    main()