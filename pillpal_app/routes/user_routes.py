from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from pillpal_app.models.user import User
from pillpal_app.database import db

# Create user blueprint
user_blueprint = Blueprint('user', __name__)

def serialize_user(user):
    """Helper function to serialize user data."""
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "address": user.address,
        "phone_number": user.phone_number,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }

# Fetch all users
@user_blueprint.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [serialize_user(user) for user in users]
    return jsonify(users_list), 200

# Get a user by ID
@user_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(serialize_user(user)), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Create a new user
@user_blueprint.route('', methods=['POST'])
def create_user():
    data = request.get_json()

    # Validate required fields
    required_fields = ['username', 'email', 'password', 'address', 'phone_number']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Field '{field}' is required"}), 400

    if '@' not in data['email']:
        return jsonify({"error": "Invalid email format"}), 400

    if not data['phone_number'].isdigit():
        return jsonify({"error": "Phone number must contain only digits"}), 400

    # Create a new User object
    new_user = User(
        username=data['username'],
        email=data['email'],
        address=data['address'],
        phone_number=data['phone_number']
    )
    new_user.set_password(data['password'])  # Hash the password

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 400

    return jsonify(serialize_user(new_user)), 201

# Update a user (PATCH)
@user_blueprint.route('/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    # Update fields if provided
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        if '@' not in data['email']:
            return jsonify({"error": "Invalid email format"}), 400
        user.email = data['email']
    if 'address' in data:
        user.address = data['address']
    if 'phone_number' in data:
        if not data['phone_number'].isdigit():
            return jsonify({"error": "Phone number must contain only digits"}), 400
        user.phone_number = data['phone_number']
    if 'password' in data:
        user.set_password(data['password'])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 400

    return jsonify(serialize_user(user)), 200

# Delete a user (DELETE)
@user_blueprint.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)

        # Check if the user exists
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Try to delete the user
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"}), 200

        except IntegrityError:
            # Handle integrity errors (e.g., foreign key constraints)
            db.session.rollback()
            return jsonify({
                "error": "Cannot delete user. Associated records exist."
            }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"An unexpected error occurred: {str(e)}"
        }), 500

        

