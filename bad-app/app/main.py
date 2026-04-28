from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

def is_strong_password(password: str) -> bool:
    # BUG: Validation logic flaw - accepts passwords that contain ANY digit
    # even if too short (e.g., "1" would pass, but should not)
    return len(password) >= 8 or any(char.isdigit() for char in password)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    if not data or "username" not in data or "password" not in data:
        raise BadRequest("username and password are required")

    if not is_strong_password(data["password"]):
        raise BadRequest("password too weak")

    return jsonify(username=data["username"], status="registered"), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
