from pillpal_app.database import db
from pillpal_app.models.user import User
from pillpal_app.models.order import Order
from pillpal_app.models.payment import Payment
from pillpal_app.models.product import Product
from pillpal_app.models.order_item import OrderItem
from pillpal_app import create_app
from datetime import datetime

# Create app and bcrypt instance
app = create_app()

with app.app_context():
    # Drop all existing tables and recreate them 
    db.drop_all()
    db.create_all()

    # Seed Users
    user1 = User(
        username="john_doe",
        email="john@example.com",
        address="123 Elm Street, Springfield",
        phone_number="1234567890"
    )
    user1.set_password("password123")

    user2 = User(
        username="jane_doe",
        email="jane@example.com",
        address="456 Oak Avenue, Shelbyville",
        phone_number="0987654321"
    )
    user2.set_password("securepass")

    db.session.add_all([user1, user2])

    # Seed Products
    product1 = Product(
        name="Pill A",
        description="Pain reliever",
        price=10.99,
        stock_quantity=100
    )
    product2 = Product(
        name="Pill B",
        description="Fever reducer",
        price=7.99,
        stock_quantity=200
    )
    product3 = Product(
        name="Pill C",
        description="Vitamin supplement",
        price=5.49,
        stock_quantity=150
    )
    db.session.add_all([product1, product2, product3])

    # Seed Orders
    order1 = Order(
        user_id=1,  # john_doe
        total_amount=31.47,
        status="pending",
        created_at=datetime.utcnow()
    )
    order2 = Order(
        user_id=2,  # jane_doe
        total_amount=15.98,
        status="delivered",
        created_at=datetime.utcnow()
    )
    db.session.add_all([order1, order2])

    # Seed OrderItems
    order_item1 = OrderItem(
        order_id=1,  # order1
        product_id=1,  # Pill A
        quantity=2,
        price_per_unit=10.99
    )
    order_item2 = OrderItem(
        order_id=1,  # order1
        product_id=3,  # Pill C
        quantity=1,
        price_per_unit=5.49
    )
    order_item3 = OrderItem(
        order_id=2,  # order2
        product_id=2,  # Pill B
        quantity=2,
        price_per_unit=7.99
    )
    db.session.add_all([order_item1, order_item2, order_item3])

    # Seed Payments
    payment1 = Payment(
        order_id=1,  # order1
        amount=31.47,
        payment_method="credit_card",
        payment_status="completed",
        transaction_date=datetime.utcnow()
    )
    payment2 = Payment(
        order_id=2,  # order2
        amount=15.98,
        payment_method="paypal",
        payment_status="completed",
        transaction_date=datetime.utcnow()
    )
    db.session.add_all([payment1, payment2])

    # Commit all changes
    db.session.commit()

    print("Database seeded successfully!")
