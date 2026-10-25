from app.blockchain import ThreatBlockchain

blockchain = ThreatBlockchain()

# Add a sample threat record.
blockchain.create_block({
    "source": "CISA KEV",
    "cve": "CVE-2025-0001",
    "category": "sql_injection",
    "ml_prediction": "sql_injection"
})

print("Test 1 - Before tampering:")
print("Chain valid:", blockchain.verify_chain())

# Change the data in the second block without recalculating its hash.
blockchain.chain[1]["data"]["category"] = "modified_category"

print("\nTest 2 - After tampering:")
print("Chain valid:", blockchain.verify_chain()) 
