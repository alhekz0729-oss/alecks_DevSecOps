from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200

@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json()
    if data is None or "message" not in data:
        raise BadRequest("JSON body must contain 'message'")

    message = str(data["message"]).strip()
    return jsonify(message=message), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
