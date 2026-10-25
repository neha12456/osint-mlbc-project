import requests
import json
from pathlib import Path
from datetime import datetime, timezone

CISA_URL = (
    "https://www.cisa.gov/sites/default/files/feeds/"
    "known_exploited_vulnerabilities.json"
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_FILE = DATA_DIR / "cisa_kev.json"


def collect_cisa_data():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    try:
        response = requests.get(
            CISA_URL,
            headers={
                "User-Agent": "OSINT-MLBC-Student-Project/1.0"
            },
            timeout=30
        )
        response.raise_for_status()

        catalog = response.json()
        vulnerabilities = catalog.get("vulnerabilities", [])

        with OUTPUT_FILE.open("w", encoding="utf-8") as file:
            json.dump(catalog, file, indent=2, ensure_ascii=False)

        return {
            "success": True,
            "source": "CISA KEV",
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "total_vulnerabilities": len(vulnerabilities),
            "saved_to": str(OUTPUT_FILE),
            "message": "Public vulnerability data collected successfully."
        }

    except (requests.RequestException, ValueError) as error:
        return {
            "success": False,
            "source": "CISA KEV",
            "message": str(error)
        }


if __name__ == "__main__":
    result = collect_cisa_data()
    print(json.dumps(result, indent=2)) 
