from flask import Blueprint, request, jsonify
from db import db
from models import User
from utils.validators import validate_email

auth_bp = Blueprint('auth', __name__)

# Error responses
INVALID_CREDENTIALS = {"error": "Invalid email or password"}, 401
MISSING_FIELDS = {"error": "Missing required fields"}, 400
INVALID_EMAIL = {"error": "Invalid email format"}, 400
EMAIL_EXISTS = {"error": "Email already registered"}, 409

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['email', 'password']):
        return jsonify(MISSING_FIELDS)
    
    # Validate email format
    if not validate_email(data['email']):
        return jsonify(INVALID_EMAIL)
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify(EMAIL_EXISTS)
    
    # Create new user
    try:
        user = User(email=data['email'])
        user.password = data['password']  # This will hash the password
        db.session.add(user)
        db.session.commit()
        
        # Generate auth token
        token = user.generate_auth_token()
        return jsonify({
            'message': 'User registered successfully',
            'token': token
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['email', 'password']):
        return jsonify(MISSING_FIELDS)
    
    # Find user by email
    user = User.query.filter_by(email=data['email']).first()
    
    # Verify user exists and password is correct
    if user and user.verify_password(data['password']):
        token = user.generate_auth_token()
        print(f"DEBUG: Generated token type: {type(token)}, token: {token[:20] if token else 'None'}...")
        response_data = {
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email
            }
        }
        print(f"DEBUG: Response data: {response_data}")
        return jsonify(response_data), 200
    else:
        print(f"DEBUG: Login failed - user: {user}, password_match: {user.verify_password(data['password']) if user else 'N/A'}")
    
    return jsonify(INVALID_CREDENTIALS)
