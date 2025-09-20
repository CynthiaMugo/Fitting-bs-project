from flask import Blueprint,jsonify,request,send_from_directory
from app.models import User,Measurement,Product,Order,OrderItem
from app.db import db
import re
import os

# create student blueprint
fitting_bp=Blueprint("fitting",__name__,url_prefix="/fitting")

@fitting_bp.route("/products",methods=["GET"])
def get_products():
    products=Product.query.all()
    products_list=[{
        "id":product.id,
        "name":product.name,
        "description":product.description,
        "price":product.price,
        "stock":product.stock,
        "image_url":product.image_url,
        "category":product.category
    }for product in products]
    return jsonify({
        "count": len(products_list),
        "products": products_list }), 200

@fitting_bp.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "image_url": product.image_url,
        "category": product.category
    }), 200

@fitting_bp.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")
    price = data.get("price")
    stock = data.get("stock", 0)
    category = data.get("category", "")
    image_url = data.get("image_url", "")

    if not name or price is None:
        return jsonify({"error": "Name and price are required"}), 400

    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category=category,
        image_url=image_url
    )
    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product created!",
        "id": product.id,
        "name": product.name
    }), 201

@fitting_bp.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)

    db.session.commit()

    return jsonify({"message": f"Product with id {id} updated!"}), 200

@fitting_bp.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": f"Product with id {id} deleted!"}), 200

@fitting_bp.route("/measurements", methods=['POST'])
def add_measurement():
    data = request.get_json()
    user_id = int(data.get('user_id'))
    bust = data.get('bust')
    underbust = data.get('underbust')
    cup_size = data.get('cup_size')
    band_size = data.get('band_size', None)

    if not user_id or not bust or not underbust or not cup_size:
        return jsonify({"error": "All fields are required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    measurement = Measurement.query.filter_by(user_id=user_id).first()
    if measurement:
        measurement.bust = bust
        measurement.underbust = underbust
        measurement.cup_size = cup_size
        measurement.band_size = band_size
    else:
        measurement = Measurement(
            bust=bust,
            underbust=underbust,
            cup_size=cup_size,
            band_size=band_size,
            user_id=user_id
        )
        db.session.add(measurement)
    db.session.commit()

    return jsonify({
        "message": "Measurement added!",
        "id": measurement.id
    }), 201

@fitting_bp.route("/measurements/<int:user_id>", methods=["GET"])
def get_measurement(user_id):
    measurement = Measurement.query.filter_by(user_id=user_id).first()
    if not measurement:
        return jsonify({"error": "No measurements found for this user"}), 404

    return jsonify({
        "id": measurement.id,
        "user_id": measurement.user_id,
        "bust": measurement.bust,
        "underbust": measurement.underbust,
        "cup_size": measurement.cup_size,
        "band_size": measurement.band_size
    }), 200


