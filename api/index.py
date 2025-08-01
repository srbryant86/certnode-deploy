from flask import Flask, request, jsonify
import datetime
import os
import json

app = Flask(__name__)


# Main logic injection
def certify_agent(text):
    length = len(text)
    logic_density = sum(1 for c in text if c.isalpha()) / (length or 1)
    tier = min(16, int(logic_density * 10))
    confidence = round(len(text) / 200 * 0.8 + 0.1, 2)
    return {
        "input": text,
        "status": "certified",
        "tier": tier,
        "confidence": confidence,
    }


@app.route("/api/certify", methods=["POST"])
def certify():
    data = request.get_json()
    result = certify_agent(data.get("text", ""))
    return jsonify(result)


@app.route("/api/validate", methods=["POST"])
def validate():
    return jsonify({"valid": True})


@app.route("/api/batch", methods=["POST"])
def batch():
    return jsonify({"batch": "processed"})


@app.route("/api/gpt", methods=["POST"])
def gpt():
    data = request.get_json()
    model = data.get("model", "claude")
    text = data.get("text", "")

    result = certify_agent(text)
    if isinstance(result, dict):
        result["model"] = model
    else:
        result = {
            "model": model,
            "input": text,
            "status": "error",
            "message": "certify_agent failed",
        }

    return jsonify(result)


@app.route("/api/audit", methods=["POST"])
def audit():
    data = request.get_json()
    text = data.get("text", "")
    logic_density = sum(1 for c in text if c.isalpha()) / max(len(text), 1)
    tier = min(16, max(0, int(logic_density * 16)))
    audit_report = {
        "input": text,
        "logic_density": round(logic_density, 3),
        "estimated_tier": tier,
        "length": len(text),
        "status": "audited",
    }
    return jsonify(audit_report)


@app.route("/api/compare", methods=["POST"])
def compare():
    data = request.get_json()
    text1 = data.get("text1", "")
    text2 = data.get("text2", "")

    def score(text):
        return sum(1 for c in text if c.isalpha()) / max(len(text), 1)

    score1 = score(text1)
    score2 = score(text2)
    better = "text1" if score1 > score2 else "text2"

    return jsonify(
        {
            "text1_score": round(score1, 3),
            "text2_score": round(score2, 3),
            "preferred": better,
            "status": "compared",
        }
    )


@app.route("/api/vault", methods=["POST"])
def vault():
    data = request.get_json()
    text = data.get("text", "")
    model = data.get("model", "unknown")
    status = data.get("status", "unverified")
    tier = data.get("tier", 0)
    confidence = data.get("confidence", 0)

    log = {
        "text": text,
        "model": model,
        "status": status,
        "tier": tier,
        "confidence": confidence,
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }

    filename = f"runtime/logs/vault_{datetime.datetime.utcnow().isoformat()}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(log, f, indent=2)

    return jsonify({"saved": True, "path": filename})


@app.route("/api/claim", methods=["POST"])
def claim():
    data = request.get_json()
    user_id = data.get("user_id", "anonymous")
    text = data.get("text", "")

    log = {
        "user_id": user_id,
        "text": text,
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }

    filename = (
        f"runtime/claims/claim_{user_id}_{datetime.datetime.utcnow().isoformat()}.json"
    )
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(log, f, indent=2)

    return jsonify({"received": True, "user": user_id})


@app.route("/api/explain", methods=["POST"])
def explain():
    data = request.get_json()
    text = data.get("text", "")
    logic_density = sum(1 for c in text if c.isalpha()) / (len(text) + 1)
    estimated_tier = round(len(text) * logic_density / 20)

    explanation = {
        "input": text,
        "logic_density": round(logic_density, 2),
        "estimated_tier": estimated_tier,
        "reason": f"Text length and symbol ratio suggest tier {estimated_tier} based on current CertNode logic heuristics.",
        "status": "explained",
    }

    return jsonify(explanation)
