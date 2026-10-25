from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_FILE = BASE_DIR / "models" / "vulnerability_classifier.joblib"

model = joblib.load(MODEL_FILE)

samples = [
    "A SQL injection vulnerability allows an attacker to access a database.",
    "An operating system command injection flaw allows remote command execution.",
    "A vulnerability allows an attacker to escalate privileges."
]

print("OSINT-MLBC Vulnerability Classification Test\n")

for description in samples:
    prediction = model.predict([description])[0]
    print(f"Description: {description}")
    print(f"Predicted category: {prediction}\n") 
