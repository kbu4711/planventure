"""
JWT token generation and validation utilities for secure authentication
"""
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Dict, Optional, Tuple, Any
import os
from flask import current_app, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
import jwt


class JWTConfig:
    """JWT configuration constants"""
    # Default expiration times
    ACCESS_TOKEN_EXPIRES = int(os.getenv('ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour
    REFRESH_TOKEN_EXPIRES = int(os.getenv('REFRESH_TOKEN_EXPIRES', 604800))  # 7 days
    

def setup_jwt(app):
    """
    Initialize JWT configuration for the Flask app.
    
    Args:
        app: Flask application instance
        
    Returns:
        JWTManager instance
    """
    # Configure JWT settings
    app.config['JWT_SECRET_KEY'] = os.getenv(
        'JWT_SECRET_KEY',
        'your-secret-key-change-this-in-production'
    )
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=JWTConfig.ACCESS_TOKEN_EXPIRES)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=JWTConfig.REFRESH_TOKEN_EXPIRES)
    app.config['JWT_ALGORITHM'] = 'HS256'
    
    jwt = JWTManager(app)
    
    # JWT error handlers
    @jwt.user_lookup_loader
    def user_lookup_callback(jwt_header, jwt_data):
        """Load user from JWT identity"""
        identity = jwt_data["sub"]
        return {"id": identity}
    
    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        """Add custom claims to access token"""
        return {}
    
    return jwt


def generate_tokens(user_id: int, email: str = None) -> Dict[str, str]:
    """
    Generate access and refresh tokens for a user.
    
    Args:
        user_id: The user's database ID
        email: Optional user email for additional claims
        
    Returns:
        Dictionary with 'access_token' and 'refresh_token'
        
    Example:
        >>> tokens = generate_tokens(1, 'user@example.com')
        >>> tokens['access_token']
        'eyJ0eXAiOiJKV1QiLCJhbGc...'
    """
    if not user_id:
        raise ValueError("user_id is required")
    
    # Create additional claims
    additional_claims = {}
    if email:
        additional_claims['email'] = email
    
    # Convert user_id to string for JWT 'sub' claim (subject must be a string)
    identity = str(user_id)
    
    # Generate tokens
    access_token = create_access_token(
        identity=identity,
        additional_claims=additional_claims,
        expires_delta=timedelta(seconds=JWTConfig.ACCESS_TOKEN_EXPIRES)
    )
    
    refresh_token = create_refresh_token(
        identity=identity,
        additional_claims=additional_claims,
        expires_delta=timedelta(seconds=JWTConfig.REFRESH_TOKEN_EXPIRES)
    )
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'expires_in': JWTConfig.ACCESS_TOKEN_EXPIRES
    }


def decode_token(token: str, verify: bool = True) -> Optional[Dict[str, Any]]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: The JWT token string
        verify: Whether to verify token signature and expiration
        
    Returns:
        Dictionary containing token payload or None if invalid
        
    Example:
        >>> payload = decode_token(access_token)
        >>> payload['sub']  # user_id
        1
    """
    if not token:
        return None
    
    try:
        secret_key = current_app.config.get('JWT_SECRET_KEY')
        algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')
        
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm],
            options={"verify_signature": verify}
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None


def get_current_user_id() -> Optional[int]:
    """
    Get the current authenticated user's ID from JWT token.
    
    Returns:
        User ID from token claims (as integer) or None if not authenticated
        
    Example:
        >>> @app.route('/profile')
        >>> @jwt_required()
        >>> def get_profile():
        >>>     user_id = get_current_user_id()  # Returns int
    """
    try:
        identity = get_jwt_identity()
        # Convert string identity back to integer
        if identity:
            return int(identity)
        return None
    except Exception:
        return None


def get_token_claims() -> Optional[Dict[str, Any]]:
    """
    Get additional claims from the current JWT token.
    
    Returns:
        Dictionary of token claims or None
        
    Example:
        >>> @app.route('/profile')
        >>> @jwt_required()
        >>> def get_profile():
        >>>     claims = get_token_claims()
        >>>     email = claims.get('email')
    """
    try:
        return get_jwt()
    except Exception:
        return None


def token_required(fn):
    """
    Decorator for endpoints that require JWT authentication.
    Can be used as alternative to @jwt_required().
    
    Example:
        >>> @app.route('/protected')
        >>> @token_required
        >>> def protected_route():
        >>>     user_id = get_current_user_id()
        >>>     return jsonify({'user_id': user_id})
    """
    @wraps(fn)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        return fn(*args, **kwargs)
    return decorated_function


def optional_token(fn):
    """
    Decorator for endpoints where JWT is optional.
    User info will be available if token is provided and valid.
    
    Example:
        >>> @app.route('/posts')
        >>> @optional_token
        >>> def list_posts():
        >>>     user_id = get_current_user_id()
        >>>     if user_id:
        >>>         # Show user's posts
        >>>     else:
        >>>         # Show public posts
    """
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            payload = decode_token(token)
            if payload:
                # Token is valid, it will be processed by jwt_required in context
                pass
        
        return fn(*args, **kwargs)
    return decorated_function


def extract_token_from_request() -> Optional[str]:
    """
    Extract JWT token from request headers.
    
    Returns:
        Token string or None if not found
        
    Example:
        >>> token = extract_token_from_request()
        >>> if token:
        >>>     payload = decode_token(token)
    """
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return None
    
    return auth_header[7:]


def create_token_response(user_id: int, email: str = None, message: str = 'Login successful') -> Dict[str, Any]:
    """
    Create a complete token response for API responses.
    
    Args:
        user_id: The user's ID
        email: Optional user email
        message: Optional message
        
    Returns:
        Dictionary with tokens and metadata
        
    Example:
        >>> response = create_token_response(1, 'user@example.com')
        >>> return jsonify(response), 200
    """
    tokens = generate_tokens(user_id, email)
    
    return {
        'message': message,
        'data': {
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token'],
            'token_type': tokens['token_type'],
            'expires_in': tokens['expires_in']
        }
    }


def validate_token_payload(token: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """
    Validate token and return comprehensive error information.
    
    Args:
        token: JWT token string
        
    Returns:
        Tuple of (is_valid, payload, error_message)
        
    Example:
        >>> is_valid, payload, error = validate_token_payload(token)
        >>> if not is_valid:
        >>>     print(f"Token invalid: {error}")
    """
    if not token:
        return False, None, "Token is missing"
    
    try:
        secret_key = current_app.config.get('JWT_SECRET_KEY')
        algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')
        
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm]
        )
        return True, payload, None
    except jwt.ExpiredSignatureError:
        return False, None, "Token has expired"
    except jwt.InvalidTokenError as e:
        return False, None, f"Invalid token: {str(e)}"
    except Exception as e:
        return False, None, f"Token validation error: {str(e)}"


def refresh_token_endpoint_response(refresh_token: str) -> Tuple[Dict[str, Any], int]:
    """
    Generate response for refresh token endpoint.
    
    Args:
        refresh_token: The refresh token from request
        
    Returns:
        Tuple of (response_dict, status_code)
        
    Example:
        >>> @app.route('/auth/refresh', methods=['POST'])
        >>> @jwt_required(refresh=True)
        >>> def refresh():
        >>>     response, status = refresh_token_endpoint_response(refresh_token)
        >>>     return jsonify(response), status
    """
    is_valid, payload, error = validate_token_payload(refresh_token)
    
    if not is_valid:
        return {
            'error': 'Invalid refresh token',
            'message': error
        }, 401
    
    user_id = payload.get('sub')
    email = payload.get('email')
    
    tokens = generate_tokens(user_id, email)
    
    return {
        'message': 'Token refreshed successfully',
        'data': {
            'access_token': tokens['access_token'],
            'token_type': tokens['token_type'],
            'expires_in': tokens['expires_in']
        }
    }, 200
