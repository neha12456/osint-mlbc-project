import json
from pathlib import Path

import joblib

from app.blockchain import ThreatBlockchain

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "cisa_kev.json"
MODEL_FILE = BASE_DIR / "models" / "vulnerability_classifier.joblib"


def main():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        catalog = json.load(file)

    model = joblib.load(MODEL_FILE)
    blockchain = ThreatBlockchain()

    vulnerabilities = catalog.get("vulnerabilities", [])
    processed = 0

    for item in vulnerabilities[:20]:
        name = item.get("vulnerabilityName", "")
        description = item.get("shortDescription", "")
        cve = item.get("cveID", "")

        text = f"{name} {description}"
        prediction = str(model.predict([text])[0])

        blockchain.create_block({
            "source": "CISA KEV",
            "cve": cve,
            "vulnerability_name": name,
            "ml_category": prediction
        })

        processed += 1

    print("OSINT-MLBC integration completed.")
    print(f"Records processed: {processed}")
    print(f"Total blocks: {len(blockchain.chain)}")
    print(f"Blockchain valid: {blockchain.verify_chain()}")
    print(f"Ledger: {BASE_DIR / 'data' / 'threat_blockchain.json'}")


if __name__ == "__main__":
    main()
