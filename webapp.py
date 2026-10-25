from flask import Flask, render_template, jsonify
from pathlib import Path
import json
import joblib

from app.blockchain import ThreatBlockchain

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "cisa_kev.json"
MODEL_FILE = BASE_DIR / "models" / "vulnerability_classifier.joblib"

web_app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "app" / "templates")
)


def get_records():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        catalog = json.load(file)

    model = joblib.load(MODEL_FILE)
    records = []

    for item in catalog.get("vulnerabilities", []):
        name = item.get("vulnerabilityName", "")
        description = item.get("shortDescription", "")

        records.append({
            "cve": item.get("cveID", ""),
            "name": name,
            "description": description,
            "vendor": item.get("vendorProject", ""),
            "product": item.get("product", ""),
            "date_added": item.get("dateAdded", ""),
            "category": str(
                model.predict([f"{name} {description}"])[0]
            )
        })

    return records


@web_app.route("/")
def index():
    records = get_records()
    blockchain = ThreatBlockchain()

    return render_template(
        "index.html",
        records=records[:100],
        total_records=len(records),
        total_blocks=len(blockchain.chain),
        chain_valid=blockchain.verify_chain()
    )


@web_app.route("/api/threats")
def api_threats():
    return jsonify(get_records()[:100])


@web_app.route("/api/blockchain")
def api_blockchain():
    blockchain = ThreatBlockchain()

    return jsonify({
        "total_blocks": len(blockchain.chain),
        "valid": blockchain.verify_chain(),
        "blocks": blockchain.chain
    })


if __name__ == "__main__":
    web_app.run(host="127.0.0.1", port=5000, debug=False)
