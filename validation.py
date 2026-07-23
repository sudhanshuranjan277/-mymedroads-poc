def check_field(data, field):
    """
    Check whether a field is available in records.
    """

    for item in data:

        value = item.get(field, "")

        if not value or str(value).strip() == "":
            return False

    return True



def validate(hospital_data, doctors_data):
    """
    Validate hospital and doctor scraped data.
    """

    print("\n========== Validation Report ==========")


    # =====================================
    # DOCTOR VALIDATION
    # =====================================

    print("\nDOCTOR VALIDATION")
    print("-----------------")


    total_doctors = len(doctors_data)

    print(
        f"Total Doctors        : {total_doctors}"
    )


    # Duplicate doctor names

    names = [
        doctor.get("doctor_name", "").strip()
        for doctor in doctors_data
        if doctor.get("doctor_name")
    ]


    duplicate_names = len(names) - len(set(names))


    print(
        f"Duplicate Names      : {duplicate_names}"
    )


    # Missing doctor names

    missing_names = sum(
        1
        for doctor in doctors_data
        if not doctor.get("doctor_name")
    )


    print(
        f"Missing Names        : {missing_names}"
    )


    # Missing profile URL

    missing_profile = sum(
        1
        for doctor in doctors_data
        if not doctor.get("profile_url")
    )


    print(
        f"Missing Profile URL  : {missing_profile}"
    )


    # =====================================
    # FIELD CHECK
    # =====================================

    print("\n\nFIELD CHECK")
    print("-----------")


    required_fields = [

        "doctor_name",
        "designation",
        "department",
        "qualification",
        "summary"

    ]


    for field in required_fields:


        status = check_field(
            doctors_data,
            field
        )


        if status:

            result = "PASS"

        else:

            result = "PARTIAL"


        print(
            f"{field:<20}: {result}"
        )



    # =====================================
    # HOSPITAL VALIDATION
    # =====================================

    print("\n\nHOSPITAL VALIDATION")
    print("-------------------")


    if hospital_data:


        hospital = hospital_data[0]


        required_hospital_fields = [

            "hospital_name",
            "address",
            "website"

        ]


        for field in required_hospital_fields:


            if hospital.get(field):

                result = "PASS"

            else:

                result = "FAIL"


            label = field.replace(
                "_",
                " "
            ).title()


            print(
                f"{label:<20}: {result}"
            )


    else:

        print(
            "Hospital Data Missing"
        )



    print("\n=======================================")

    print(
        "Validation Completed Successfully"
    )

    print(
        "=======================================\n"
    )