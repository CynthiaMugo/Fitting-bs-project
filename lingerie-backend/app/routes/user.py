from flask import Blueprint,jsonify,request,send_from_directory
from app.models import User,Measurement,Product,Order,OrderItem
from app.db import db
import re
import os
from flask_jwt_extended import jwt_required, get_jwt_identity

# create order blueprint
user_bp=Blueprint("user",__name__, url_prefix="/user")

@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200

# ------------------------
# Update user profile
# ------------------------
@user_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json() or {}

    username = data.get("username")
    email = data.get("email")

    # Basic validations
    if username:
        if len(username) < 3:
            return jsonify({"error": "Username must be at least 3 characters"}), 400
        user.username = username

    if email:
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(email_regex, email):
            return jsonify({"error": "Invalid email format"}), 400
        user.email = email

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

# ------------------------
# Delete user account
# ------------------------
@user_bp.route("/me", methods=["DELETE"])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted successfully"}), 200


