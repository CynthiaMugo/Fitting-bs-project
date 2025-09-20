from app import create_app
from app.db import db
from app.models import User, Product, Order, OrderItem, Measurement
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
app = create_app()

with app.app_context():
    print("Clearing tables...")
    db.drop_all()
    db.create_all()

    print("Seeding users...")
    user1 = User(
        username="cynthia",
        email="cynthia@example.com",
        password_hash=bcrypt.generate_password_hash("password123").decode("utf-8"),
    )
    user2 = User(
        username="mike",
        email="mike@example.com",
        password_hash=bcrypt.generate_password_hash("password456").decode("utf-8"),
    )

    db.session.add_all([user1, user2])
    db.session.commit()

    print("Seeding measurements...")
    measurement1 = Measurement(
        bust=36.5, underbust=32.0, cup_size="C", band_size="32", user_id=user1.id
    )
    measurement2 = Measurement(
        bust=38.0, underbust=34.0, cup_size="D", band_size="34", user_id=user2.id
    )

    db.session.add_all([measurement1, measurement2])
    db.session.commit()

    print("Seeding products...")
    product1 = Product(
        name="Lace Bra",
        description="Elegant lace bra with adjustable straps",
        price=29.99,
        stock=50,
        image_url="https://example.com/lace-bra.jpg",
        category="Bras",
    )
    product2 = Product(
        name="Silk Nightgown",
        description="Smooth silk nightgown for comfort",
        price=59.99,
        stock=20,
        image_url="https://example.com/silk-nightgown.jpg",
        category="Nightwear",
    )

    db.session.add_all([product1, product2])
    db.session.commit()

    print("Seeding orders...")
    order1 = Order(user_id=user1.id, status="pending")
    order2 = Order(user_id=user2.id, status="shipped")

    db.session.add_all([order1, order2])
    db.session.commit()

    print("Seeding order items...")
    order_item1 = OrderItem(order_id=order1.id, product_id=product1.id, quantity=1)
    order_item2 = OrderItem(order_id=order2.id, product_id=product2.id, quantity=2)

    db.session.add_all([order_item1, order_item2])
    db.session.commit()

    print("Seeding complete!")
