from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "CertNode API is live"

@app.route('/certify', methods=['POST'])
def certify():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "Missing text"}), 400
    
    # Placeholder logic
    return jsonify({
        "input": text,
        "status": "certified",
        "tier": 12,
        "confidence": 0.92
    })

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    content = data.get('content', '')
    if not content:
        return jsonify({"error": "Missing content"}), 400
    
    # Placeholder logic
    return jsonify({
        "input": content,
        "valid": True,
        "notes": "Structure conforms to CertNode Tier 14 criteria."
    })

@app.route('/batch', methods=['POST'])
def batch():
    data = request.get_json()
    items = data.get('texts', [])
    if not isinstance(items, list):
        return jsonify({"error": "Expected list of texts"}), 400

    results = [{
        "input": item,
        "certified": True,
        "tier": 13
    } for item in items]

    return jsonify({"results": results})
