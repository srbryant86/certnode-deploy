
from flask import Flask, request, jsonify
from main import run_certnode_pipeline

app = Flask(__name__)

@app.route("/certify", methods=["POST"])
def certify():
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    result = run_certnode_pipeline(data["text"])
    return jsonify({
        "tier": result["tier"],
        "hash": result["hash"],
        "certified_output": result["certified_output"],
        "reflex": result["reflex"],
        "audit": result["audit"]
    })

@app.route("/", methods=["GET"])
def index():
    return "CertNode API is online."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
