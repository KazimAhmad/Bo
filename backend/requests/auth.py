from flask import jsonify, request, session, send_from_directory
import sys
sys.path.append("../config/config.py")
sys.path.append("../models/user.py")
sys.path.append("../requests/token.py")

from config.config import db, app, bcrypt
from models.user import User
from requests import token

#this is a decorater which goes above the function that we are gonna write
@app.route("/users", methods = ["GET"])
def users():
    users = User.query.all()
    json_users = list(map(lambda user: user.to_json(), users))
    
    return jsonify(
        {
            "users": json_users
        }
    )

#create a user
@app.route("/users/sign-up", methods = ["POST"])
def create_user():
    new_user_name = request.json.get("userName")
    new_email = request.json.get("email")
    new_password = request.json.get("password")
    
    if not new_user_name:
        return jsonify(
            {
                "error": "A valid user name is required"
            }
        ), 400
    elif not new_email:
         return jsonify(
            {
                "error": "A valid email is required"
            }
        ), 400
    elif not new_password:
         return jsonify(
            {
                "error": "A valid password is required"
            }
        ), 400
    #same username or email validation
    same_user_name = User.query.filter_by(new_user_name).first()
    if same_user_name:
        return jsonify(
            {
                "error": "a user with same username already exists"
            }
        ), 400
    same_email = User.query.filter_by(new_email).first()
    if same_email:
        return jsonify(
            {
                "error": "a user with same email already exists"
            }
        ), 400

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    new_user = User(user_name = new_user_name,
                    email = new_email,
                    password = hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "User Created"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify(
            { "message": "Missing credentials" }
            ), 400
    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(
        user_name = username
    ).first()

    print(user)
    if not user:
        return jsonify(
            { "message": "No user found with this username" }
        ), 404
    
    saved_pass = user.password
    print(saved_pass)

    if not bcrypt.check_password_hash(saved_pass, password):
        return jsonify(
            { "message": "wrong password" }
        ), 400
    
    new_token, refresh_token = token.generate_tokens(username)

    return jsonify({
        "token": new_token,
        "refresh_token": refresh_token,
        "user": user.to_json()
        }), 200