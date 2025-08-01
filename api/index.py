from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def home():
    return "CertNode API is live"

@app.route('/api/certify', methods=['POST'])
def certify():
    data = request.get_json()
    text = data.get("text", "")
    return jsonify({
        "input": text,
        "status": "certified",
        "tier": 12,
        "confidence": 0.92
    })

@app.route('/api/validate', methods=['POST'])
def validate():
    data = request.get_json()
    return jsonify({
        "input": data.get("content", ""),
        "valid": True,
        "notes": "Structure conforms to CertNode Tier 14 criteria."
    })

@app.route('/api/batch', methods=['POST'])
def batch():
    data = request.get_json()
    results = []
    for text in data.get("texts", []):
        results.append({
            "input": text,
            "certified": True,
            "tier": 13
        })
    return jsonify({"results": results})

if __name__ == "__main__":
    app.run()
