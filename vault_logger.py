import hashlib
import json
from datetime import datetime

def emit_vault_log(content, tier, valence, recursion, confidence):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "tier": tier,
        "valence": valence,
        "recursion": recursion,
        "confidence": confidence,
        "content_hash": hashlib.sha256(content.encode()).hexdigest()
    }

    with open("vault_certified_audits.jsonl", "a") as f:
        f.write(json.dumps(record) + "\n")

    return record["content_hash"]
