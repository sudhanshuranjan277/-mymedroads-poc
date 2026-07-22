import os


def save_doctors_sql(doctors, filename="doctors.sql"):
    os.makedirs("output", exist_ok=True)

    filepath = os.path.join("output", filename)

    with open(filepath, "w", encoding="utf-8") as f:

        f.write("DELETE FROM doctors;\n\n")

        for d in doctors:

            doctor_name = d["doctor_name"].replace("'", "''")
            specialty = d["specialty"].replace("'", "''")
            profile = d["profile_url"].replace("'", "''")
            appointment = d["appointment_url"].replace("'", "''")

            f.write(
                f"""INSERT INTO doctors
(doctor_id,hospital_id,doctor_name,specialty,profile_url,appointment_url)
VALUES
({d['doctor_id']},
 {d['hospital_id']},
 '{doctor_name}',
 '{specialty}',
 '{profile}',
 '{appointment}');

"""
            )

    print(f"✅ SQL saved: {filepath}")