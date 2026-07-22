import json
import os


def save_json(data, filename):
    os.makedirs("output", exist_ok=True)

    filepath = os.path.join("output", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ JSON saved: {filepath}")