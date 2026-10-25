import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LEDGER_FILE = BASE_DIR / "data" / "threat_blockchain.json"


class ThreatBlockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()

        if not self.chain:
            self.create_block({
                "message": "OSINT-MLBC blockchain initialized"
            })

    @staticmethod
    def calculate_hash(block):
        block_data = {
            "index": block["index"],
            "timestamp": block["timestamp"],
            "data": block["data"],
            "previous_hash": block["previous_hash"]
        }

        encoded = json.dumps(
            block_data,
            sort_keys=True,
            separators=(",", ":")
        ).encode("utf-8")

        return hashlib.sha256(encoded).hexdigest()

    def create_block(self, data):
        previous_hash = (
            self.chain[-1]["hash"] if self.chain else "0"
        )

        block = {
            "index": len(self.chain),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data,
            "previous_hash": previous_hash
        }

        block["hash"] = self.calculate_hash(block)
        self.chain.append(block)
        self.save_chain()

        return block

    def save_chain(self):
        LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)

        with LEDGER_FILE.open("w", encoding="utf-8") as file:
            json.dump(self.chain, file, indent=2, ensure_ascii=False)

    def load_chain(self):
        if LEDGER_FILE.exists():
            try:
                with LEDGER_FILE.open("r", encoding="utf-8") as file:
                    loaded = json.load(file)

                if isinstance(loaded, list):
                    self.chain = loaded
            except (json.JSONDecodeError, OSError):
                self.chain = []

    def verify_chain(self):
        for position, block in enumerate(self.chain):
            if block["index"] != position:
                return False

            if block["hash"] != self.calculate_hash(block):
                return False

            expected_previous = (
                self.chain[position - 1]["hash"]
                if position > 0 else "0"
            )

            if block["previous_hash"] != expected_previous:
                return False

        return True


if __name__ == "__main__":
    blockchain = ThreatBlockchain()

    print("OSINT-MLBC Blockchain Test")
    print(f"Total blocks: {len(blockchain.chain)}")
    print(f"Chain valid: {blockchain.verify_chain()}")
    print(f"Ledger saved to: {LEDGER_FILE}") 
