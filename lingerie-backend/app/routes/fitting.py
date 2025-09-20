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