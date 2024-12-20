from flask import Blueprint, request, jsonify
from pillpal_app.database import db
from pillpal_app.models.order import Order
from pillpal_app.models.order_item import OrderItem
from pillpal_app.models.payment import Payment
from sqlalchemy.exc import SQLAlchemyError

order_routes = Blueprint('order', __name__)

# Utility function to serialize an order
def serialize_order(order):
    return {
        "id": order.id,
        "user_id": order.user_id,
        "total_amount": order.total_amount,
        "status": order.status,
        "created_at": order.created_at,
        "order_items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price_per_unit": item.price_per_unit,
                "total_price": item.total_price
            }
            for item in order.order_items
        ],
        "payment": {
            "id": order.payment.id,
            "amount": order.payment.amount,
            "payment_method": order.payment.payment_method,
            "payment_status": order.payment.payment_status.value,
            "transaction_date": order.payment.transaction_date
        } if order.payment else None
    }


# Get all orders
@order_routes.route('', methods=['GET'])
def get_orders():
    try:
        orders = Order.query.all()
        return jsonify([serialize_order(order) for order in orders]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


# Get a single order by ID
@order_routes.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
        return jsonify(serialize_order(order)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


# Create a new order
@order_routes.route('/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        user_id = data['user_id']
        total_amount = data['total_amount']
        order_items = data.get('order_items', [])
        
        # Create the order
        new_order = Order(user_id=user_id, total_amount=total_amount)
        db.session.add(new_order)
        db.session.flush()  # Get the new order ID before committing

        # Add order items
        for item in order_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price_per_unit=item['price_per_unit']
            )
            db.session.add(order_item)
        
        # create payment records
        payment_data = data.get('payment')
        if payment_data:
            payment = Payment(
                order_id=new_order.id,
                amount=payment_data['amount'],
                payment_method=payment_data['payment_method']
            )
            db.session.add(payment)
        
        db.session.commit()
        return jsonify(serialize_order(new_order)), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400


# Update an order
@order_routes.route('/orders/<int:order_id>', methods=['PATCH'])
def update_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
        
        data = request.get_json()

        # Update order fields
        if 'total_amount' in data:
            order.total_amount = data['total_amount']
        if 'status' in data:
            order.status = data['status']

        # Update or add order items
        if 'order_items' in data:
            # Delete existing order items
            OrderItem.query.filter_by(order_id=order_id).delete()
            
            # Add new order items
            for item in data['order_items']:
                order_item = OrderItem(
                    order_id=order_id,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    price_per_unit=item['price_per_unit']
                )
                db.session.add(order_item)

        # Update payment details
        if 'payment' in data:
            payment_data = data['payment']
            if order.payment:
                order.payment.amount = payment_data.get('amount', order.payment.amount)
                order.payment.payment_method = payment_data.get('payment_method', order.payment.payment_method)
                order.payment.payment_status = payment_data.get('payment_status', order.payment.payment_status)
            else:
                payment = Payment(
                    order_id=order_id,
                    amount=payment_data['amount'],
                    payment_method=payment_data['payment_method']
                )
                db.session.add(payment)

        db.session.commit()
        return jsonify(serialize_order(order)), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Delete an order
@order_routes.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
        
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
