import jwt
from flask import jsonify, request
from config.config import app
from functools import wraps
from datetime import datetime
import jwt

def generate_tokens(username):
    payload = {
        "sub": username,  # subject (who the token is for)
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "type": "access"
    }

    refresh_payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        "type": "refresh"
    }

    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, app.config["SECRET_KEY"], algorithm="HS256")

    return token, refresh_token

@app.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json()
    refresh_token = data.get("refresh_token")

    try:
        payload = jwt.decode(refresh_token, app.config["SECRET_KEY"], algorithms=["HS256"])

        if payload["type"] != "refresh":
            return {"message": "Invalid token type"}, 401

        new_access = jwt.encode(
            {
                "sub": payload["sub"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=15),
                "type": "access"
            },
            app.config["SECRET_KEY"],
            algorithm="HS256"
        )

        return {"access_token": new_access}

    except jwt.ExpiredSignatureError:
        return {"message": "Refresh token expired"}, 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "Token missing"}), 401

        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise ValueError("Invalid auth scheme")

            payload = jwt.decode(
                token,
                app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            request.user = payload["sub"]

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except Exception:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated

@app.route("/protected")
@token_required
def protected():
    return jsonify({
        "message": "Access granted",
        "user": request.user
    })