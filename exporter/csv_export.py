import os
import pandas as pd


def export_to_csv(hospital_data, doctors_data, output_dir="output"):
    """
    Export hospital and doctor data to CSV files.
    """

    os.makedirs(output_dir, exist_ok=True)

    hospital_df = pd.DataFrame(hospital_data)
    doctor_df = pd.DataFrame(doctors_data)

    hospital_path = os.path.join(output_dir, "hospital.csv")
    doctor_path = os.path.join(output_dir, "doctors.csv")

    hospital_df.to_csv(
        hospital_path,
        index=False,
        encoding="utf-8-sig"
    )

    doctor_df.to_csv(
        doctor_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"✅ Hospital CSV saved: {hospital_path}")
    print(f"✅ Doctor CSV saved: {doctor_path}")