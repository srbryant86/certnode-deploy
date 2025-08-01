from flask import Flask

app = Flask(__name__)


@app.route("/api")
def certnode_api():
    return "CertNode API is live"
