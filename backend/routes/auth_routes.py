from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({
        'message': 'Login successful',
        'token': f"mock-jwt-token-{user.id}-{user.username}",
        'user': user.to_dict()
    }), 200

@auth_bp.route('/me', methods=['GET'])
def me():
    # Return current active user details
    user = User.query.first()
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'username': 'analyst', 'role': 'Security Analyst'}), 200
