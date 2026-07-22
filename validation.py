def validate(doctors_data):
    """
    Basic validation for scraped doctor data.
    """

    print("\n========== Validation Report ==========")

    total = len(doctors_data)
    print(f"Total Doctors: {total}")

    # Duplicate name check
    names = [d.get("doctor_name", "").strip() for d in doctors_data]

    duplicates = len(names) - len(set(names))

    if duplicates == 0:
        print("✅ No duplicate doctor names found.")
    else:
        print(f"❌ Duplicate doctor names found: {duplicates}")

    # Missing mandatory fields
    mandatory = ["doctor_name", "specialty", "profile_url"]

    missing = 0

    for doctor in doctors_data:
        for field in mandatory:
            if not doctor.get(field):
                missing += 1

    if missing == 0:
        print("✅ All mandatory fields are present.")
    else:
        print(f"⚠ Missing mandatory fields: {missing}")

    print("=======================================\n")