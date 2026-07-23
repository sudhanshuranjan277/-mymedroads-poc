import os


def save_doctors_sql(
        doctors,
        filename="doctors.sql"
):

    os.makedirs(
        "output",
        exist_ok=True
    )


    filepath = os.path.join(
        "output",
        filename
    )


    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:


        f.write(
            "DELETE FROM doctors;\n\n"
        )



        for d in doctors:


            doctor_name = d.get(
                "doctor_name",
                ""
            ).replace(
                "'",
                "''"
            )


            specialty = d.get(
                "specialty",
                ""
            ).replace(
                "'",
                "''"
            )


            department = d.get(
                "department",
                ""
            ).replace(
                "'",
                "''"
            )


            hospital_name = d.get(
                "hospital_name",
                "Artemis Hospitals"
            ).replace(
                "'",
                "''"
            )


            profile = d.get(
                "profile_url",
                ""
            ).replace(
                "'",
                "''"
            )



            f.write(

                f"""
INSERT INTO doctors
(
doctor_id,
hospital_id,
hospital_name,
doctor_name,
department,
specialty,
profile_url
)
VALUES
(
{d.get("doctor_id", 0)},
{d.get("hospital_id", 0)},
'{hospital_name}',
'{doctor_name}',
'{department}',
'{specialty}',
'{profile}'
);

"""

            )


    print(
        f"✅ SQL saved: {filepath}"
    )