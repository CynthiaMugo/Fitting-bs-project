from flask import Blueprint,jsonify,request,send_from_directory
from app.models import User,Measurement,Product,Order,OrderItem
from app.db import db
import re
import os

# create order blueprint
order_bp=Blueprint("order",__name__)

@order_bp.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    user_id = data.get("user_id")
    items = data.get("items")  # list of {product_id, quantity}

    if not user_id or not items:
        return jsonify({"error": "user_id and items are required"}), 400
    new_order = Order(user_id=user_id, status="pending")
    db.session.add(new_order)
    db.session.flush()
    for item in items:
        product_id = item.get("product_id")
        quantity = item.get("quantity", 1)

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(order_item)

    db.session.commit()

    return jsonify({
        "message": "Order created",
        "order": {
            "id": new_order.id,
            "user_id": new_order.user_id,
            "status": new_order.status,
            "items": [
                {"product_id": i.product_id, "quantity": i.quantity}
                for i in new_order.items
            ]
        }
    }), 201


@order_bp.route("/orders/<int:user_id>", methods=["GET"])
def get_orders(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()

    orders_list = []
    for order in orders:
        order_data = {
            "id": order.id,
            "status": order.status,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity
                }
                for item in order.items 
            ]
        }
        orders_list.append(order_data)

    return jsonify(orders_list), 200

