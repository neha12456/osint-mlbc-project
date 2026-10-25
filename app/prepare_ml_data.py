import re
import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "ml_training_dataset.csv"
OUTPUT_FILE = BASE_DIR / "data" / "ml_category_dataset.csv"


def classify_vulnerability(row):
    text = " ".join([
        str(row.get("vulnerability_name", "")),
        str(row.get("description", ""))
    ]).lower()

    rules = [
        ("sql_injection", r"sql injection"),
        ("command_injection", r"command injection|os command injection"),
        ("remote_code_execution", r"remote code execution|\brce\b"),
        ("cross_site_scripting", r"cross.site scripting|\bxss\b"),
        ("privilege_escalation", r"privilege escalation|gain elevated privileges"),
        ("path_traversal", r"path traversal|directory traversal"),
        ("authentication", r"authentication bypass|bypass authentication"),
        ("information_disclosure", r"information disclosure|sensitive information"),
    ]

    for label, pattern in rules:
        if re.search(pattern, text):
            return label

    return "other"


def main():
    df = pd.read_csv(INPUT_FILE)
    df["category"] = df.apply(classify_vulnerability, axis=1)

    df.to_csv(OUTPUT_FILE, index=False)

    print("ML category dataset created.")
    print(f"Records: {len(df)}")
    print(f"Saved to: {OUTPUT_FILE}")
    print("\nCategory counts:")
    print(df["category"].value_counts().to_string())


if __name__ == "__main__":
    main() 
