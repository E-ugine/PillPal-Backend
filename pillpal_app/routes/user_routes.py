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
