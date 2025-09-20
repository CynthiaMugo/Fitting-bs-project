from flask import Blueprint,jsonify,request,send_from_directory
from app.models import User,Measurement,Product,Order,OrderItem
from app.db import db
from app import bcrypt
import re
import os
from flask_jwt_extended import create_access_token

# create student blueprint
authentication_bp=Blueprint("authentication",__name__,url_prefix="/authentication")

@authentication_bp.route("/register",methods=["POST"])
def register():
    data=request.get_json()
    username=data.get("username")
    email=data.get("email")
    password=data.get("password")

    if not username or not email or not password:
        return jsonify({"error":"Username, email, and password are required"}),400

    if User.query.filter_by(email=email).first():
        return jsonify({"error":"Email already registered"}),400

    if User.query.filter_by(username=username).first():
        return jsonify({"error":"Username already taken"}),400

    if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
        return jsonify({"error":"Invalid email format"}),400

    password_hash=bcrypt.generate_password_hash(password).decode("utf-8")
    new_user=User(username=username,email=email,password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created!",
        "user": {"id": new_user.id, "username": new_user.username, "email": new_user.email}
    }), 201

@authentication_bp.route("/login",methods=["POST"])
def login():
    data=request.get_json()
    email=data.get("email")
    password=data.get("password")

    if not email or not password:
        return jsonify({"error":"Email and password are required"}),400

    user=User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash,password):
        return jsonify({"error":"Invalid email or password"}),401
    # Generate JWT token
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200