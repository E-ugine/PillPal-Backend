from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from pillpal_app.models.product import Product
from pillpal_app.database import db

# Create product blueprint
product_blueprint = Blueprint('product', __name__)

def serialize_product(product):
    """Helper function to serialize product data."""
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock_quantity": product.stock_quantity,
        "created_at": product.created_at,
        "updated_at": product.updated_at
    }

# Get products
@product_blueprint.route('', methods=['GET'])
def get_products():
    products = Product.query.all()
    products_list = [serialize_product(product) for product in products]
    return jsonify(products_list), 200

# Get a product by ID
@product_blueprint.route('/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(serialize_product(product)), 200
    else:
        return jsonify({"error": "Product not found"}), 404

# Create a new product
@product_blueprint.route('', methods=['POST'])
def create_product():
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'price', 'stock_quantity']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Field '{field}' is required"}), 400

    if data['price'] < 0:
        return jsonify({"error": "Price must be non-negative"}), 400

    if data['stock_quantity'] < 0:
        return jsonify({"error": "Stock quantity must be non-negative"}), 400

    # Create a new Product object
    new_product = Product(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        stock_quantity=data['stock_quantity']
    )

    try:
        db.session.add(new_product)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Failed to add product"}), 400

    return jsonify(serialize_product(new_product)), 201

# Update a product
@product_blueprint.route('/<int:product_id>', methods=['PATCH'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()

    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        if data['price'] < 0:
            return jsonify({"error": "Price must be non-negative"}), 400
        product.price = data['price']
    if 'stock_quantity' in data:
        if data['stock_quantity'] < 0:
            return jsonify({"error": "Stock quantity must be non-negative"}), 400
        product.stock_quantity = data['stock_quantity']

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Failed to update product"}), 400

    return jsonify(serialize_product(product)), 200

# Delete a product
@product_blueprint.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
