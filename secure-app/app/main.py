from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="healthy"), 200

@app.route("/mode", methods=["GET"])
def mode():
    return jsonify(mode=os.getenv("SERVICE_MODE", "production")), 200

@app.route("/echo", methods=["POST"])
def echo():
    payload = request.get_json(silent=True)
    if not payload or "message" not in payload:
        return jsonify(error="JSON body must contain 'message'"), 400
    return jsonify(message=str(payload["message"]).strip()), 200

@app.route("/external", methods=["GET"])
def external():
    response = requests.get("https://httpbin.org/get", timeout=5)
    return jsonify(status=response.status_code, origin=response.json().get("origin")), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
