import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "cisa_kev.json"
OUTPUT_FILE = BASE_DIR / "data" / "ml_training_dataset.csv"


def prepare_dataset():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        catalog = json.load(file)

    records = catalog.get("vulnerabilities", [])
    rows = []

    for item in records:
        name = item.get("vulnerabilityName", "")
        description = item.get("shortDescription", "")
        vendor = item.get("vendorProject", "")
        product = item.get("product", "")
        required_action = item.get("requiredAction", "")

        # Initial heuristic label based on CISA's KEV inclusion.
        # This label represents catalog membership, not attack detection.
        label = "known_exploited"

        rows.append({
            "vulnerability_name": name,
            "description": description,
            "vendor": vendor,
            "product": product,
            "required_action": required_action,
            "label": label
        })

    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset=["vulnerability_name", "vendor", "product"])
    df.to_csv(OUTPUT_FILE, index=False)

    print("Dataset prepared successfully.")
    print(f"Records: {len(df)}")
    print(f"Saved to: {OUTPUT_FILE}")
    print("\nLabel counts:")
    print(df["label"].value_counts())


if __name__ == "__main__":
    prepare_dataset()
