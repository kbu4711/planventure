"""
Authentication middleware for protecting routes with JWT tokens.
Provides decorators and utilities for route protection.
"""
from functools import wraps
from flask import request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from jwt import DecodeError, ExpiredSignatureError
import logging

logger = logging.getLogger(__name__)


def protected_route(fn):
    """
    Decorator to protect routes and require JWT authentication.
    
    Usage:
        @app.route('/api/protected')
        @protected_route
        def protected_endpoint():
            user_id = get_jwt_identity()
            return {'message': f'Hello user {user_id}'}
    
    Returns:
        401 Unauthorized if no token or invalid token
        403 Forbidden if token is invalid/expired
    """
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        try:
            # Get current user info from JWT
            user_id = get_jwt_identity()
            jwt_claims = get_jwt()
            
            # Store in g for access in route handler
            g.user_id = user_id
            g.jwt_claims = jwt_claims
            
            # Call the actual route handler
            return fn(*args, **kwargs)
        
        except ExpiredSignatureError:
            return jsonify({
                'error': 'token_expired',
                'message': 'Your session has expired. Please login again.'
            }), 401
        
        except DecodeError:
            return jsonify({
                'error': 'invalid_token',
                'message': 'Invalid or malformed token.'
            }), 401
        
        except Exception as e:
            logger.error(f"Auth middleware error: {str(e)}")
            return jsonify({
                'error': 'auth_error',
                'message': 'Authentication failed.'
            }), 401
    
    return wrapper


def optional_auth(fn):
    """
    Decorator for routes that work with or without authentication.
    If a valid token is provided, user info is available in g.user_id.
    If no token, route still executes but g.user_id is None.
    
    Usage:
        @app.route('/api/optional-auth')
        @optional_auth
        def endpoint():
            if g.user_id:
                return {'message': f'Authenticated as {g.user_id}'}
            return {'message': 'Anonymous access'}
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # Check if Authorization header exists
            auth_header = request.headers.get('Authorization', '')
            
            if auth_header.startswith('Bearer '):
                try:
                    # Try to validate token
                    from flask_jwt_extended import verify_jwt_in_request
                    verify_jwt_in_request()
                    
                    # Token is valid
                    g.user_id = get_jwt_identity()
                    g.jwt_claims = get_jwt()
                
                except (ExpiredSignatureError, DecodeError):
                    # Token exists but is invalid/expired - still allow access
                    # but set user_id to None
                    g.user_id = None
                    g.jwt_claims = None
            else:
                # No token provided
                g.user_id = None
                g.jwt_claims = None
            
            # Call the actual route handler
            return fn(*args, **kwargs)
        
        except Exception as e:
            logger.error(f"Optional auth middleware error: {str(e)}")
            g.user_id = None
            g.jwt_claims = None
            return fn(*args, **kwargs)
    
    return wrapper


def require_roles(*roles):
    """
    Decorator to require specific user roles.
    
    Usage:
        @app.route('/api/admin')
        @protected_route
        @require_roles('admin')
        def admin_only():
            return {'message': 'Admin area'}
    
    Args:
        *roles: Required role(s). User must have at least one.
    
    Returns:
        403 Forbidden if user doesn't have required role
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                jwt_claims = get_jwt()
                user_roles = jwt_claims.get('roles', [])
                
                # Check if user has at least one required role
                if not any(role in user_roles for role in roles):
                    return jsonify({
                        'error': 'insufficient_permissions',
                        'message': f'This endpoint requires one of: {", ".join(roles)}'
                    }), 403
                
                return fn(*args, **kwargs)
            
            except Exception as e:
                logger.error(f"Role check error: {str(e)}")
                return jsonify({
                    'error': 'auth_error',
                    'message': 'Authorization check failed.'
                }), 403
        
        return wrapper
    
    return decorator


def get_current_user_id():
    """
    Get current authenticated user ID from g.user_id.
    Converts string ID from JWT back to integer.
    
    Returns:
        User ID (int) if authenticated, None otherwise
    """
    user_id = getattr(g, 'user_id', None)
    if user_id is not None:
        return int(user_id)
    return None


def is_authenticated():
    """
    Check if current request is authenticated.
    
    Returns:
        True if user is authenticated, False otherwise
    """
    return get_current_user_id() is not None


def get_auth_header():
    """
    Extract Bearer token from Authorization header.
    
    Returns:
        Token string if present, None otherwise
    """
    auth_header = request.headers.get('Authorization', '')
    
    if auth_header.startswith('Bearer '):
        return auth_header[7:]  # Remove 'Bearer ' prefix
    
    return None
