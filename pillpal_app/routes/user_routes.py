from flask import Blueprint, jsonify, request
from pillpal_app.models.user import User
from pillpal_app.database import db

#create user blueprint
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

@user_blueprint.route('', methods=['GET'])
def get_users():
    user_id = request.args.get('id')  # Fetch 'id' from query params if provided
    
    if user_id:
        try:
            user_id = int(user_id)  # Ensure user_id is an integer
        except ValueError:
            return jsonify({"error": "Invalid user ID format"}), 400

        # Fetch a single user by id
        user = User.query.get(user_id)
        if user:
            return jsonify(serialize_user(user)), 200
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        # Fetch all users
        users = User.query.all()
        users_list = [serialize_user(user) for user in users]
        return jsonify(users_list), 200
