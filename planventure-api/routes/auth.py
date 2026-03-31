"""
Authentication routes for user registration and login
"""
from flask import Blueprint, request, jsonify
from database import db
from models.user import User
from schemas import user_register_schema, user_login_schema
from jwt_utils import generate_tokens, create_token_response
from password_utils import is_password_strong
from marshmallow import ValidationError
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def validate_email_format(email: str) -> tuple[bool, str]:
    """
    Validate email format using regex.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"
    
    # RFC 5322 simplified regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return False, "Invalid email format"
    
    if len(email) > 255:
        return False, "Email is too long (max 255 characters)"
    
    return True, ""


def check_email_exists(email: str) -> bool:
    """
    Check if email already exists in database.
    
    Args:
        email: Email to check
        
    Returns:
        True if email exists, False otherwise
    """
    return db.session.query(User.query.filter_by(email=email).exists()).scalar()


def register_user(email: str, password: str) -> tuple[dict, int]:
    """
    Register a new user with email and password.
    
    This is a helper function that can be called programmatically or from routes.
    
    Args:
        email: User's email address
        password: User's password
        
    Returns:
        Tuple of (response_dict, status_code)
        - response_dict contains 'data' with user info and tokens on success,
          or 'error', 'message', and additional fields on failure
        - status_code is HTTP status (201 for success, 400/409/500 for errors)
    """
    try:
        # Normalize email
        email = email.lower().strip()
        
        # Validate email format
        email_valid, email_error = validate_email_format(email)
        if not email_valid:
            return {
                'error': 'validation_error',
                'message': 'Email validation failed',
                'details': email_error
            }, 400
        
        # Check if email already registered
        if check_email_exists(email):
            return {
                'error': 'email_exists',
                'message': 'This email is already registered. Please use a different email or login.'
            }, 409
        
        # Validate password strength
        strength = is_password_strong(password)
        if not strength['is_strong']:
            requirements = []
            if not strength['length']:
                requirements.append("Password must be at least 8 characters long")
            if not strength['has_uppercase']:
                requirements.append("Password must contain at least one uppercase letter")
            if not strength['has_lowercase']:
                requirements.append("Password must contain at least one lowercase letter")
            if not strength['has_digit']:
                requirements.append("Password must contain at least one digit")
            if not strength['has_special']:
                requirements.append("Password must contain at least one special character (!@#$%^&*)")
            
            return {
                'error': 'weak_password',
                'message': 'Password does not meet strength requirements',
                'requirements': requirements,
                'score': strength['score']
            }, 400
        
        # Create new user
        user = User(email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Generate tokens
        tokens = generate_tokens(user.id, user.email)
        
        # Prepare response
        response = {
            'message': 'User registered successfully',
            'data': {
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'created_at': user.created_at.isoformat()
                },
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token'],
                'token_type': tokens['token_type'],
                'expires_in': tokens['expires_in']
            }
        }
        
        return response, 201
    
    except Exception as e:
        db.session.rollback()
        return {
            'error': 'server_error',
            'message': 'An error occurred during registration. Please try again.'
        }, 500


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user account.
    
    Request body (JSON):
    {
        "email": "user@example.com",
        "password": "SecurePass123!"
    }
    
    Returns:
    {
        "message": "User registered successfully",
        "data": {
            "user": {
                "id": 1,
                "email": "user@example.com"
            },
            "access_token": "...",
            "refresh_token": "...",
            "token_type": "Bearer",
            "expires_in": 3600
        }
    }
    
    Status codes:
    - 201: Registration successful
    - 400: Invalid input or validation error
    - 409: Email already registered
    - 500: Server error
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'validation_error',
                'message': 'Request body must be valid JSON'
            }), 400
        
        # Validate input schema
        try:
            validated_data = user_register_schema.load(data)
        except ValidationError as err:
            return jsonify({
                'error': 'validation_error',
                'message': 'Invalid input data',
                'errors': err.messages
            }), 400
        
        email = validated_data.get('email', '')
        password = validated_data.get('password', '')
        
        # Call helper function
        response, status_code = register_user(email, password)
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({
            'error': 'server_error',
            'message': 'An error occurred during registration. Please try again.'
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint.
    
    Request body (JSON):
    {
        "email": "user@example.com",
        "password": "SecurePass123!"
    }
    
    Returns:
    {
        "message": "Login successful",
        "data": {
            "user": {
                "id": 1,
                "email": "user@example.com"
            },
            "access_token": "...",
            "refresh_token": "...",
            "token_type": "Bearer",
            "expires_in": 3600
        }
    }
    
    Status codes:
    - 200: Login successful
    - 400: Invalid input
    - 401: Invalid credentials
    - 500: Server error
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'validation_error',
                'message': 'Request body must be valid JSON'
            }), 400
        
        # Validate input schema
        try:
            validated_data = user_login_schema.load(data)
        except ValidationError as err:
            return jsonify({
                'error': 'validation_error',
                'message': 'Invalid input data',
                'errors': err.messages
            }), 400
        
        email = validated_data.get('email', '').lower().strip()
        password = validated_data.get('password', '')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({
                'error': 'invalid_credentials',
                'message': 'Invalid email or password'
            }), 401
        
        # Generate tokens
        tokens = generate_tokens(user.id, user.email)
        
        # Prepare response
        response = {
            'message': 'Login successful',
            'data': {
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'created_at': user.created_at.isoformat()
                },
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token'],
                'token_type': tokens['token_type'],
                'expires_in': tokens['expires_in']
            }
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            'error': 'server_error',
            'message': 'An error occurred during login. Please try again.'
        }), 500


@auth_bp.route('/validate-email', methods=['POST'])
def validate_email():
    """
    Validate email format and availability.
    
    Request body (JSON):
    {
        "email": "user@example.com"
    }
    
    Returns:
    {
        "email": "user@example.com",
        "is_valid": true,
        "is_available": true,
        "message": "Email is valid and available"
    }
    
    Status codes:
    - 200: Validation complete
    - 400: Invalid input
    """
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({
                'error': 'validation_error',
                'message': 'Email is required'
            }), 400
        
        email = data.get('email', '').lower().strip()
        
        # Validate email format
        is_valid, error_msg = validate_email_format(email)
        
        if not is_valid:
            return jsonify({
                'email': email,
                'is_valid': False,
                'is_available': False,
                'message': error_msg
            }), 200
        
        # Check availability
        is_available = not check_email_exists(email)
        
        return jsonify({
            'email': email,
            'is_valid': True,
            'is_available': is_available,
            'message': 'Email is available' if is_available else 'Email is already registered'
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'server_error',
            'message': 'An error occurred during email validation'
        }), 500


@auth_bp.route('/check-password-strength', methods=['POST'])
def check_password_strength():
    """
    Check password strength without registering.
    
    Request body (JSON):
    {
        "password": "TestPass123!"
    }
    
    Returns:
    {
        "is_strong": true,
        "score": 5,
        "requirements": {
            "length": true,
            "has_uppercase": true,
            "has_lowercase": true,
            "has_digit": true,
            "has_special": true
        },
        "message": "Password is strong"
    }
    
    Status codes:
    - 200: Check complete
    - 400: Invalid input
    """
    try:
        data = request.get_json()
        
        if not data or 'password' not in data:
            return jsonify({
                'error': 'validation_error',
                'message': 'Password is required'
            }), 400
        
        password = data.get('password', '')
        
        if not password:
            return jsonify({
                'error': 'validation_error',
                'message': 'Password cannot be empty'
            }), 400
        
        # Check strength
        strength = is_password_strong(password)
        
        # Build requirements summary
        requirements = {
            'length': strength['length'],
            'has_uppercase': strength['has_uppercase'],
            'has_lowercase': strength['has_lowercase'],
            'has_digit': strength['has_digit'],
            'has_special': strength['has_special']
        }
        
        message = 'Password is strong' if strength['is_strong'] else 'Password does not meet all strength requirements'
        
        return jsonify({
            'is_strong': strength['is_strong'],
            'score': strength['score'],
            'requirements': requirements,
            'message': message
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'server_error',
            'message': 'An error occurred during password strength check'
        }), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Logout endpoint.
    
    Currently a placeholder - in production, you might:
    - Invalidate tokens on server
    - Add token to blacklist
    - Log user activity
    
    Returns:
    {
        "message": "Logout successful"
    }
    
    Status codes:
    - 200: Logout successful
    """
    return jsonify({
        'message': 'Logout successful'
    }), 200
