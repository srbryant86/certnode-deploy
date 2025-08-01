from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/api", methods=["GET"])
def root():
    return "CertNode API is live"


@app.route("/api/certify", methods=["POST"])
def certify():
    data = request.get_json()
    return jsonify(
        {
            "input": data.get("text", ""),
            "status": "certified",
            "tier": 12,
            "confidence": 0.92,
        }
    )


@app.route("/api/validate", methods=["POST"])
def validate():
    return jsonify({"valid": True})


@app.route("/api/batch", methods=["POST"])
def batch():
    return jsonify({"batch": "processed"})
